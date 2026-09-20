import httpx
from fastapi import APIRouter, Request

from api.core.http_client import get_http_client
from api.core.rate_limit import limiter
from bot.bhiss_collector import BASE_URL, BROWSER_HEADERS

router = APIRouter(tags=["observability"])


@router.get("/health")
@limiter.limit("30/minute")
async def health(request: Request) -> dict:
    bhiss_status = "ok"
    try:
        client = get_http_client(request.app.state)
        response = await client.get(
            BASE_URL, headers=BROWSER_HEADERS, timeout=5.0, follow_redirects=True
        )
        response.raise_for_status()
    except httpx.HTTPError:
        bhiss_status = "down"

    return {
        "status": "ok" if bhiss_status == "ok" else "degraded",
        "bhiss": bhiss_status,
    }
