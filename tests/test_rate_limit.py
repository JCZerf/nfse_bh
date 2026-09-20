def test_requests_beyond_limit_are_rejected(api_client):
    api_key = "chave-exclusiva-teste-rate-limit"

    statuses = [api_client.get("/metrics", headers={"X-API-Key": api_key}).status_code for _ in range(35)]

    assert statuses.count(200) == 30
    assert statuses.count(429) == 5


def test_rate_limit_is_isolated_per_key(api_client):
    key_a = "chave-a-teste-rate-limit"
    key_b = "chave-b-teste-rate-limit"

    for _ in range(31):
        api_client.get("/metrics", headers={"X-API-Key": key_a})

    response_a = api_client.get("/metrics", headers={"X-API-Key": key_a})
    response_b = api_client.get("/metrics", headers={"X-API-Key": key_b})

    assert response_a.status_code == 429
    assert response_b.status_code == 200
