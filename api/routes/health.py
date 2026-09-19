import httpx
from fastapi import APIRouter, Request

from bot.bhiss_collector import BASE_URL, BROWSER_HEADERS

from api.rate_limit import limiter

router = APIRouter(tags=["observability"])


@router.get("/health")
@limiter.limit("30/minute")
async def health(request: Request) -> dict:
    bhiss_status = "ok"
    try:
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
            response = await client.get(BASE_URL, headers=BROWSER_HEADERS)
            response.raise_for_status()
    except httpx.HTTPError:
        bhiss_status = "down"

    return {
        "status": "ok" if bhiss_status == "ok" else "degraded",
        "bhiss": bhiss_status,
    }
