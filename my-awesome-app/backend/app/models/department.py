from datetime import datetime
from sqlalchemy import BigInteger, String, SmallInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.models.base import BaseModel
from app.database import Base


class Department(Base, BaseModel):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("departments.id", ondelete="CASCADE"), nullable=True, index=True
    )
    sort: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    leader: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)

    children: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="parent",
        lazy="selectin",
        order_by="Department.sort",
    )
    parent: Mapped[Optional["Department"]] = relationship(
        "Department",
        back_populates="children",
        remote_side="Department.id",
        lazy="selectin",
    )
    users: Mapped[List["User"]] = relationship("User", back_populates="department", lazy="selectin")

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', code='{self.code}')>"


from app.models.user import User
