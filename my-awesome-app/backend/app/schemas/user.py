from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: int = Field(default=1, ge=0, le=1)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_ids: List[int] = []


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    role_ids: Optional[List[int]] = None
    status: Optional[int] = Field(None, ge=0, le=1)


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: int
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    department: Optional[dict] = None
    position: Optional[dict] = None
    roles: List[dict] = []
    status: int
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class PasswordReset(BaseModel):
    temp_password: str
