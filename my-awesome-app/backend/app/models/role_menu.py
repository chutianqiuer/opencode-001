from datetime import datetime
from sqlalchemy import (
    BigInteger,
    String,
    SmallInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel
from app.database import Base


class RoleMenu(Base, BaseModel):
    __tablename__ = "role_menus"

    role_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    menu_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False, index=True
    )

    __table_args__ = (UniqueConstraint("role_id", "menu_id", name="uq_role_menu"),)

    def __repr__(self):
        return f"<RoleMenu(role_id={self.role_id}, menu_id={self.menu_id})>"
