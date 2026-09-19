from fastapi import APIRouter, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from api.rate_limit import limiter

router = APIRouter(tags=["observability"])


@router.get("/metrics")
@limiter.limit("30/minute")
async def metrics(request: Request) -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
