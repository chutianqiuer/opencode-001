from datetime import datetime
from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    SmallInteger,
    DateTime,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.models.base import BaseModel
from app.database import Base


class User(Base, BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, nullable=True, index=True
    )
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )
    position_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("positions.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="user_roles", back_populates="users", lazy="selectin"
    )
    department: Mapped[Optional["Department"]] = relationship(
        "Department", back_populates="users", lazy="selectin"
    )
    position: Mapped[Optional["Position"]] = relationship(
        "Position", back_populates="users", lazy="selectin"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}')>"


from app.models.role import Role
from app.models.department import Department
from app.models.position import Position
