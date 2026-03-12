import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
from app.database import Base
from typing import AsyncGenerator

TEST_DATABASE_URL = "mysql+aiomysql://root:root123@localhost:3306/rbac_admin_test"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

TestAsyncSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "password": "Test@123",
        "name": "Test User",
        "email": "test@example.com",
        "phone": "13800138000",
        "status": 1,
        "is_superuser": False,
    }
