import httpx
from starlette.datastructures import State


def get_http_client(state: State) -> httpx.AsyncClient:
    if not hasattr(state, "http_client"):
        state.http_client = httpx.AsyncClient()
    return state.http_client
