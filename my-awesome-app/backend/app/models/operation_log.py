from datetime import datetime
from sqlalchemy import BigInteger, String, SmallInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.models.base import BaseModel
from app.database import Base


class OperationLog(Base, BaseModel):
    __tablename__ = "operation_logs"

    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    module: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    method: Mapped[str] = mapped_column(String(10), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    params: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    error_msg: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="operation_logs", lazy="selectin"
    )

    def __repr__(self):
        return f"<OperationLog(id={self.id}, username='{self.username}', action='{self.action}')>"


from app.models.user import User
