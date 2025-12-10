# Version 1.0
# Time: Wed Dec 10, 15:24
# Backend

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models import ContactDetail, ContactModel, UpdateContactModel
import pandas as pd
import io
import re

# Yiwen Wang: 设置FastAPI前端、中间件设置和mongodb的基本连接与数据库地址
app = FastAPI()

# Yiwen Wang: 一次性获取通讯录的最大数量
max_length = 1000

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.contact_db
collection = db.contacts

# Yiwen Wang: 获取数据
@app.get("/contacts", response_model=list[ContactModel])
async def get_contacts():
    # Yiwen Wang: 先按照is_favorite星标进行倒序排序，然后再用姓名做正序排序
    # 这样就可以实现星号在前
    return await collection.find().sort([("is_favorite", -1), ("name", 1)]).to_list(max_length)

# Yiwen Wang: 插入数据
@app.post("/contacts", response_model=ContactModel)
async def create_contact(contact: ContactModel):
    new_contact = await collection.insert_one(contact.model_dump(by_alias=True, exclude=["id"]))
    
    return await collection.find_one({"_id": new_contact.inserted_id})

# Yiwen Wang: 删除数据
@app.delete("/contacts/{id}")
async def delete_contact(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"success": True}
    
    raise HTTPException(status_code=404, detail="Contact not found")

# Yiwen Wang: 更新数据
@app.put("/contacts/{id}", response_model=ContactModel)
async def update_contact(id: str, contact: UpdateContactModel):
    update_data = {k: v for k, v in contact.model_dump().items() if v is not None}

    if update_data:
        await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if (existing := await collection.find_one({"_id": ObjectId(id)})):
        return existing
    
    raise HTTPException(status_code=404, detail="Contact not found")

# Yiwen Wang: 数据导出
@app.get("/contacts/export")
async def export_contacts():
    contacts = await collection.find().to_list(max_length)
    data = []

    for c in contacts:
        # [Label] Value 使用换行分隔
        def format_field(field_list):
            return "\n".join([f"[{item['label']}] {item['value']}" for item in field_list])

        data.append({
            "姓名": c.get('name'),
            "是否收藏": "是" if c.get('is_favorite') else "否",
            "电话": format_field(c.get('phones', [])),
            "邮箱": format_field(c.get('emails', [])),
            "地址": format_field(c.get('addresses', [])),
            "社交账号": format_field(c.get('socials', []))
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    output.seek(0)
    headers = {'Content-Disposition': 'attachment; filename="contacts.xlsx"'}
    return StreamingResponse(output, headers=headers,
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')