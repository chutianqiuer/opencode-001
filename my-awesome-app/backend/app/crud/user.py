from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.user_role import UserRole
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from datetime import datetime


class CRUDUser(CRUDBase[User]):
    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.username == username).options(selectinload(User.roles))
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        user_data = obj_in.model_dump(exclude={"role_ids", "password"})
        user_data["password"] = obj_in.password

        db_obj = User(**user_data)
        db.add(db_obj)
        await db.flush()

        if obj_in.role_ids:
            for role_id in obj_in.role_ids:
                user_role = UserRole(user_id=db_obj.id, role_id=role_id)
                db.add(user_role)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate | Dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True, exclude={"role_ids"})

        role_ids = None
        if isinstance(obj_in, UserUpdate) and obj_in.role_ids is not None:
            role_ids = obj_in.role_ids

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        if role_ids is not None:
            await db.execute(select(UserRole).where(UserRole.user_id == db_obj.id))
            existing_roles = (
                (await db.execute(select(UserRole).where(UserRole.user_id == db_obj.id)))
                .scalars()
                .all()
            )

            for role in existing_roles:
                await db.delete(role)

            for role_id in role_ids:
                user_role = UserRole(user_id=db_obj.id, role_id=role_id)
                db.add(user_role)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, username: str, password: str
    ) -> Optional[User]:
        from app.utils.security import verify_password

        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def update_last_login(self, db: AsyncSession, *, user_id: int) -> None:
        user = await self.get(db, id=user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            await db.commit()

    async def get_with_roles(self, db: AsyncSession, *, user_id: int) -> Optional[User]:
        result = await db.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.roles),
                selectinload(User.department),
                selectinload(User.position),
            )
        )
        return result.scalar_one_or_none()

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        username: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[int] = None,
        department_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[User], int]:
        query = select(User).options(
            selectinload(User.roles),
            selectinload(User.department),
            selectinload(User.position),
        )

        if username:
            query = query.where(User.username.like(f"%{username}%"))
        if name:
            query = query.where(User.name.like(f"%{name}%"))
        if status is not None:
            query = query.where(User.status == status)
        if department_id:
            query = query.where(User.department_id == department_id)

        query = query.where(User.deleted_at.is_(None))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await db.execute(query)
        users = result.scalars().all()

        return users, total


async def get_user_permissions(db: AsyncSession, user_id: int) -> List[str]:
    from sqlalchemy import select, distinct
    from app.models.user_role import UserRole
    from app.models.role_menu import RoleMenu
    from app.models.menu import Menu

    query = (
        select(distinct(Menu.code))
        .select_from(Menu)
        .join(RoleMenu, RoleMenu.menu_id == Menu.id)
        .join(UserRole, UserRole.role_id == RoleMenu.role_id)
        .where(UserRole.user_id == user_id)
        .where(Menu.status == 1)
    )

    result = await db.execute(query)
    permissions = [row[0] for row in result.all()]
    return permissions


user_crud = CRUDUser(User)
