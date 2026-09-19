import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(api_key_header)) -> None:
    expected_key = os.environ.get("API_KEY")
    if not expected_key or api_key != expected_key:
        raise HTTPException(status_code=401, detail="API key invalida")
