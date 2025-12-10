# Version 1.0
# Time: Wed Dec 10, 15:21
# Models for transferring data between the frontend and the backend

from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, List, Annotated

# Yiwen Wang: 把数据库的ObjectId看成str
PyObjectId = Annotated[str, BeforeValidator(str)]

class ContactDetail(BaseModel):
    label: str = "默认"
    value: str

# Yiwen Wang: 如果需要接受多种数据，那么转为list进行存储会更好
class ContactModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    # reminder: 之后用is_favorite直接进行排序
    is_favorite: bool = False
    phones: List[ContactDetail] = []
    emails: List[ContactDetail] = []
    addresses: List[ContactDetail] = []
    socials: List[ContactDetail] = []
