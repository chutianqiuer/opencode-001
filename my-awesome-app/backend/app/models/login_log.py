from datetime import datetime
from sqlalchemy import BigInteger, String, SmallInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.models.base import BaseModel
from app.database import Base


class LoginLog(Base, BaseModel):
    __tablename__ = "login_logs"

    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    ip: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    browser: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    os: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    message: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="login_logs", lazy="selectin"
    )

    def __repr__(self):
        return f"<LoginLog(id={self.id}, username='{self.username}', status={self.status})>"


from app.models.user import User
