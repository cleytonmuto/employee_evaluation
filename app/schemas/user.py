# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from app.models.user import RoleEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    sector_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.employee

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    sector_id: Optional[UUID] = None

class UserOut(UserBase):
    id: UUID
    role: RoleEnum

    class Config:
        from_attributes = True
