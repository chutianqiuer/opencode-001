"""
Seed data for default super admin user

Revision ID: 002
Create Date: 2026-03-12
"""

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("Admin@123")

    users_table = sa.table(
        "users",
        sa.column("username", sa.String),
        sa.column("password", sa.String),
        sa.column("name", sa.String),
        sa.column("email", sa.String),
        sa.column("status", sa.SmallInteger),
        sa.column("is_superuser", sa.Boolean),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "username": "admin",
                "password": hashed_password,
                "name": "超级管理员",
                "email": "admin@example.com",
                "status": 1,
                "is_superuser": True,
            }
        ],
    )


def downgrade():
    op.execute("DELETE FROM users WHERE username = 'admin'")
