import pytest
from fastapi import HTTPException
from app.auth import verify_api_key
import app.auth as auth_module


def test_verify_api_key_success(monkeypatch):
    # Temporarily set a known API key for this test only
    monkeypatch.setattr(auth_module, "API_KEY", "test-secret-key")

    # Call the function directly with the CORRECT key
    verify_api_key(x_api_key="test-secret-key")


def test_verify_api_key_failure(monkeypatch):
    monkeypatch.setattr(auth_module, "API_KEY", "test-secret-key")

    # We EXPECT this to raise HTTPException — pytest.raises checks that
    with pytest.raises(HTTPException):
        verify_api_key(x_api_key="wrong-key")
