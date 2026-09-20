import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def api_client():
    """TestClient usado como context manager para disparar o lifespan da app
    (sem isso, app.state.http_client nunca e criado e qualquer rota que
    dependa dele quebra com AttributeError)."""
    from main import app

    with TestClient(app) as client:
        yield client
