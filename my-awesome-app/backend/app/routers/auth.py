import uuid
import base64
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    CaptchaResponse,
    TokenRefresh,
    TokenResponse,
    UserInfoResponse,
)
from app.schemas.common import ApiResponse
from app.crud.user import user_crud
from app.crud.log import login_log_crud
from app.utils.security import create_access_token, create_refresh_token, verify_token
from app.utils.captcha import generate_captcha
from app.utils.redis_client import redis_client
from app.config import settings
from app.middleware.auth import get_current_user
from typing import List


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/captcha", response_model=ApiResponse[CaptchaResponse])
async def get_captcha():
    captcha_key = str(uuid.uuid4())
    code, image_bytes = generate_captcha()
    captcha_image = base64.b64encode(image_bytes).decode("utf-8")

    await redis_client.set(
        f"captcha:{captcha_key}",
        code,
        ex=settings.CAPTCHA_EXPIRE_SECONDS,
    )

    return ApiResponse(
        code=200,
        message="success",
        data=CaptchaResponse(
            captcha_key=captcha_key,
            captcha_image=f"data:image/png;base64,{captcha_image}",
        ),
    )


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    stored_code = await redis_client.get(f"captcha:{login_data.captcha_key}")
    if not stored_code or stored_code.upper() != login_data.captcha_code.upper():
        await login_log_crud.create_log(
            db,
            user_id=None,
            username=login_data.username,
            ip=request.client.host if request.client else "unknown",
            status=0,
            message="验证码错误",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误",
        )

    await redis_client.delete(f"captcha:{login_data.captcha_key}")

    user = await user_crud.authenticate(
        db, username=login_data.username, password=login_data.password
    )

    if not user:
        await login_log_crud.create_log(
            db,
            user_id=None,
            username=login_data.username,
            ip=request.client.host if request.client else "unknown",
            status=0,
            message="用户名或密码错误",
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误",
        )

    if user.status != 1:
        await login_log_crud.create_log(
            db,
            user_id=user.id,
            username=user.username,
            ip=request.client.host if request.client else "unknown",
            status=0,
            message="账号已被禁用",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号已被禁用",
        )

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    await redis_client.set(
        f"token:refresh:{user.id}",
        refresh_token,
        ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    await user_crud.update_last_login(db, user_id=user.id)

    await login_log_crud.create_log(
        db,
        user_id=user.id,
        username=user.username,
        ip=request.client.host if request.client else "unknown",
        status=1,
        message="登录成功",
    )

    return ApiResponse(
        code=200,
        message="登录成功",
        data=LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
    )


@router.post("/logout", response_model=ApiResponse)
async def logout(
    request: Request,
    current_user=Depends(get_current_user),
):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        await redis_client.set(
            f"token:blacklist:{token}",
            "1",
            ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    await redis_client.delete(f"token:refresh:{current_user.id}")

    return ApiResponse(code=200, message="退出成功", data=None)


@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    user_id = verify_token(token_data.refresh_token, "refresh")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    stored_token = await redis_client.get(f"token:refresh:{user_id}")
    if not stored_token or stored_token != token_data.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been invalidated",
        )

    user = await user_crud.get(db, id=int(user_id))
    if not user or user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled",
        )

    access_token = create_access_token(subject=user.id)

    return ApiResponse(
        code=200,
        message="刷新成功",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ),
    )


@router.get("/user/info", response_model=ApiResponse[UserInfoResponse])
async def get_user_info(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await user_crud.get_with_roles(db, user_id=current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    department_dict = None
    if user.department:
        department_dict = {
            "id": user.department.id,
            "name": user.department.name,
        }

    position_dict = None
    if user.position:
        position_dict = {
            "id": user.position.id,
            "name": user.position.name,
        }

    roles_list = []
    permissions_set = set()

    if user.roles:
        for role in user.roles:
            roles_list.append(
                {
                    "id": role.id,
                    "name": role.name,
                    "code": role.code,
                }
            )

    if user.is_superuser:
        permissions_set.add("*:*:*")
    else:
        cached_perms = await redis_client.get(f"user:perms:{user.id}")
        if cached_perms:
            permissions_set = set(cached_perms.split(","))
        else:
            from app.crud.user import get_user_permissions

            permissions_list = await get_user_permissions(db, user.id)
            permissions_set = set(permissions_list)
            await redis_client.set(
                f"user:perms:{user.id}",
                ",".join(permissions_list),
                ex=1800,
            )

    return ApiResponse(
        code=200,
        message="success",
        data=UserInfoResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            email=user.email,
            phone=user.phone,
            avatar=user.avatar,
            department=department_dict,
            position=position_dict,
            roles=roles_list,
            permissions=list(permissions_set),
        ),
    )
