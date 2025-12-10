# Version 1.0
# Time: Wed Dec 10, 15:24
# Backend

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import pandas as pd
import io
import re

# Yiwen Wang: 设置FastAPI前端、中间件设置和mongodb的基本连接与数据库地址
app = FastAPI()

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