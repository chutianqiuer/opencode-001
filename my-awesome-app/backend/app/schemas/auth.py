from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, description="Password")
    captcha_key: str = Field(..., description="Captcha UUID")
    captcha_code: str = Field(..., description="Captcha code")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class CaptchaResponse(BaseModel):
    captcha_key: str
    captcha_image: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserInfoResponse(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    department: Optional[dict] = None
    position: Optional[dict] = None
    roles: list = []
    permissions: list = []

    class Config:
        from_attributes = True
