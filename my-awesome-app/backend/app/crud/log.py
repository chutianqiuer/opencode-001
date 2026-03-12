from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.login_log import LoginLog
from app.crud.base import CRUDBase
from datetime import datetime


class CRUDLoginLog(CRUDBase[LoginLog]):
    async def create_log(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[int],
        username: str,
        ip: str,
        location: Optional[str] = None,
        browser: Optional[str] = None,
        os: Optional[str] = None,
        status: int,
        message: Optional[str] = None,
    ) -> LoginLog:
        log_data = {
            "user_id": user_id,
            "username": username,
            "ip": ip,
            "location": location,
            "browser": browser,
            "os": os,
            "status": status,
            "message": message,
        }
        return await self.create(db, obj_in=log_data)

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        status: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[LoginLog], int]:
        query = select(LoginLog)

        if user_id:
            query = query.where(LoginLog.user_id == user_id)
        if username:
            query = query.where(LoginLog.username.like(f"%{username}%"))
        if status is not None:
            query = query.where(LoginLog.status == status)
        if start_time:
            query = query.where(LoginLog.created_at >= start_time)
        if end_time:
            query = query.where(LoginLog.created_at <= end_time)

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        query = query.offset(skip).limit(limit).order_by(LoginLog.created_at.desc())
        result = await db.execute(query)
        logs = result.scalars().all()

        return logs, total

    async def clear_all(self, db: AsyncSession) -> int:
        result = await db.execute(select(LoginLog))
        logs = result.scalars().all()
        count = len(logs)
        for log in logs:
            await db.delete(log)
        await db.commit()
        return count


login_log_crud = CRUDLoginLog(LoginLog)
