import pytest
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
)


def test_password_hashing():
    password = "TestPassword@123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    user_id = 1
    token = create_access_token(subject=user_id)
    assert token is not None
    assert isinstance(token, str)


def test_create_refresh_token():
    user_id = 1
    token = create_refresh_token(subject=user_id)
    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    user_id = 123
    token = create_access_token(subject=user_id)
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == str(user_id)
    assert payload.get("type") == "access"


def test_verify_access_token():
    user_id = 456
    token = create_access_token(subject=user_id)
    result = verify_token(token, token_type="access")
    assert result == str(user_id)


def test_verify_refresh_token():
    user_id = 789
    token = create_refresh_token(subject=user_id)
    result = verify_token(token, token_type="refresh")
    assert result == str(user_id)


def test_verify_token_wrong_type():
    user_id = 100
    access_token = create_access_token(subject=user_id)
    result = verify_token(access_token, token_type="refresh")
    assert result is None


def test_verify_invalid_token():
    invalid_token = "invalid.token.here"
    result = verify_token(invalid_token)
    assert result is None


def test_token_with_additional_claims():
    user_id = 1
    additional_claims = {"role": "admin", "permissions": ["read", "write"]}
    token = create_access_token(subject=user_id, additional_claims=additional_claims)
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("role") == "admin"
    assert payload.get("permissions") == ["read", "write"]
