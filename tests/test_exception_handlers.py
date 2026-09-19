import pytest
from fastapi.testclient import TestClient

from main import app

TEST_API_KEY = "test-key-nao-e-secreta"


@pytest.fixture(autouse=True)
def _set_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", TEST_API_KEY)


client = TestClient(app)


def _valid_headers() -> dict:
    return {"X-API-Key": TEST_API_KEY}


def test_invalid_field_format_returns_generic_message():
    response = client.post(
        "/nfse/validation",
        json={"provider_cnpj": "string", "nfse_number": "string", "verification_code": "string"},
        headers=_valid_headers(),
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "Dados invalidos"}}


def test_missing_field_returns_generic_message():
    response = client.post(
        "/nfse/validation",
        json={"provider_cnpj": "35.142.610/0001-04", "nfse_number": "202500000000118"},
        headers=_valid_headers(),
    )
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "Dados invalidos"}}


def test_empty_body_returns_generic_message():
    response = client.post("/nfse/validation", json={}, headers=_valid_headers())
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "Dados invalidos"}}


def test_no_body_returns_generic_message():
    response = client.post("/nfse/validation", headers=_valid_headers())
    assert response.status_code == 422
    assert response.json() == {"detail": {"message": "Dados invalidos"}}
