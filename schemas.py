from pydantic import BaseModel, Field
from typing import Optional

# ===== 인증 =====
class SignupIn(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, pattern=r"^[a-z0-9]+$")
    password: str = Field(..., min_length=4, max_length=20)

class UserOut(BaseModel):
    id: int
    username: str

# ===== 연락처 =====
class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=5)
    phone: str = Field(..., pattern=r"^010\d{8}$")
    addr: str = ""
    category_id: int

class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=5)
    phone: Optional[str] = Field(None, pattern=r"^010\d{8}$")
    addr: Optional[str] = None
    category_id: Optional[int] = None

class ContactOut(BaseModel):
    id: int
    name: str
    phone: str
    addr: str
    category_id: int
    category_name: str

class ContactListOut(BaseModel):
    total: int
    items: list[ContactOut]

# ===== 카테고리 =====
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=10)

class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=10)

class CategoryOut(BaseModel):
    id: int
    name: str
