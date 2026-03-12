from datetime import datetime
from sqlalchemy import BigInteger, String, SmallInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from app.models.base import BaseModel
from app.database import Base


class Position(Base, BaseModel):
    __tablename__ = "positions"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    sort: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    remark: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="position", lazy="selectin")

    def __repr__(self):
        return f"<Position(id={self.id}, name='{self.name}', code='{self.code}')>"


from app.models.user import User
