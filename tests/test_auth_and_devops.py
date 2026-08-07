import pytest
from backend.app.core.auth import SecurityService


def test_password_hashing():
    raw_password = "SecretPassword123"
    hashed = SecurityService.get_password_hash(raw_password)
    assert hashed != raw_password
    assert SecurityService.verify_password(raw_password, hashed) is True


def test_jwt_token_generation():
    token = SecurityService.create_access_token({
        "sub": "admin@company.com",
        "role": "Admin",
    })
    assert isinstance(token, str)
    assert len(token) > 20