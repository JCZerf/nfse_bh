import os
import uuid

import pytest


@pytest.fixture(autouse=True)
def _set_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", f"test-key-{uuid.uuid4().hex}")


def _valid_headers() -> dict:
    return {"X-API-Key": os.environ["API_KEY"]}


def test_requests_beyond_limit_are_rejected(api_client):
    statuses = [api_client.get("/metrics", headers=_valid_headers()).status_code for _ in range(35)]

    assert statuses.count(200) == 30
    assert statuses.count(429) == 5


def test_invalid_api_key_is_rejected(api_client):
    response = api_client.get("/metrics", headers={"X-API-Key": "wrong-key"})

    assert response.status_code == 401


def test_metrics_requires_api_key(api_client):
    response = api_client.get("/metrics")

    assert response.status_code == 401


def test_health_is_public_and_does_not_require_api_key(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_deep_health_requires_api_key(api_client):
    response = api_client.get("/health/deep")

    assert response.status_code == 401
