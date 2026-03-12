"""
Create users and login_logs tables

Revision ID: 001
Create Date: 2026-03-12
"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('avatar', sa.String(255), nullable=True),
        sa.Column('department_id', sa.BigInteger(), nullable=True),
        sa.Column('position_id', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=False, server_default='1'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )
    
    op.create_index('idx_username', 'users', ['username'])
    op.create_index('idx_email', 'users', ['email'])
    
    op.create_table(
        'login_logs',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('ip', sa.String(50), nullable=False),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('browser', sa.String(50), nullable=True),
        sa.Column('os', sa.String(50), nullable=True),
        sa.Column('status', sa.SmallInteger(), nullable=False),
        sa.Column('message', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    )
    
    op.create_index('idx_user_id', 'login_logs', ['user_id'])
    op.create_index('idx_username', 'login_logs', ['username'])
    op.create_index('idx_created_at', 'login_logs', ['created_at'])


def downgrade():
    op.drop_index('idx_created_at', 'login_logs')
    op.drop_index('idx_username', 'login_logs')
    op.drop_index('idx_user_id', 'login_logs')
    op.drop_table('login_logs')
    
    op.drop_index('idx_email', 'users')
    op.drop_index('idx_username', 'users')
    op.drop_table('users')