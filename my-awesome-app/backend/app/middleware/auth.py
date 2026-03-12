import base64
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.security import verify_token
from app.utils.redis_client import redis_client

security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    token = credentials.credentials
    user_id = verify_token(token, "access")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    blacklisted = await redis_client.exists(f"token:blacklist:{token}")
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    from app.models.user import User

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is disabled",
        )
    return user


async def get_current_active_user(
    current_user=Depends(get_current_user),
):
    if current_user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


class PermissionChecker:
    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(
        self,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        if current_user.is_superuser:
            return current_user
        cached_perms = await redis_client.get(f"user:perms:{current_user.id}")
        if cached_perms:
            permissions = cached_perms.split(",")
        else:
            from app.crud.user import get_user_permissions

            permissions = await get_user_permissions(db, current_user.id)
            await redis_client.set(
                f"user:perms:{current_user.id}",
                ",".join(permissions),
                ex=1800,
            )
        if self.permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{self.permission}' required",
            )
        return current_user


def require_permission(permission: str):
    return PermissionChecker(permission)
