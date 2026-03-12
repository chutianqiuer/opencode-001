from datetime import datetime
from sqlalchemy import BigInteger, String, SmallInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.models.base import BaseModel
from app.database import Base


class Menu(Base, BaseModel):
    __tablename__ = "menus"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("menus.id", ondelete="CASCADE"), nullable=True, index=True
    )
    path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    component: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sort: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    visible: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    cache: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    remark: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    children: Mapped[List["Menu"]] = relationship(
        "Menu",
        back_populates="parent",
        lazy="selectin",
        order_by="Menu.sort",
    )
    parent: Mapped[Optional["Menu"]] = relationship(
        "Menu",
        back_populates="children",
        remote_side="Menu.id",
        lazy="selectin",
    )
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="role_menus", back_populates="menus", lazy="selectin"
    )

    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', code='{self.code}')>"


from app.models.role import Role
