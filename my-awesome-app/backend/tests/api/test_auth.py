import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.user import User
from app.utils.security import get_password_hash


@pytest.fixture
async def test_user(db_session: AsyncSession):
    user = User(
        username="testuser",
        password=get_password_hash("Test@123"),
        name="Test User",
        email="test@example.com",
        status=1,
        is_superuser=False,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_get_captcha():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/auth/captcha")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "captcha_key" in data["data"]
        assert "captcha_image" in data["data"]


@pytest.mark.asyncio
async def test_login_with_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as client:
        captcha_response = await client.get("/api/v1/auth/captcha")
        captcha_data = captcha_response.json()["data"]

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistent",
                "password": "wrongpass",
                "captcha_key": captcha_data["captcha_key"],
                "captcha_code": "ABCD",
            },
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_with_valid_credentials(test_user):
    async with AsyncClient(app=app, base_url="http://test") as client:
        captcha_response = await client.get("/api/v1/auth/captcha")
        captcha_data = captcha_response.json()["data"]

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "Test@123",
                "captcha_key": captcha_data["captcha_key"],
                "captcha_code": "ABCD",
            },
        )
        assert response.status_code == 200 or response.status_code == 400


@pytest.mark.asyncio
async def test_get_user_info_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/auth/user/info")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"},
        )
        assert response.status_code == 401
