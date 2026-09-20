from fastapi import APIRouter, Depends, Request

from api.core.rate_limit import limiter
from api.dependencies.auth import verify_api_key
from api.models.nfse import NfseQueryRequest, NfseQueryResponse
from api.services.nfse_service import fetch_nfse_data

router = APIRouter(prefix="/nfse", tags=["nfse"], dependencies=[Depends(verify_api_key)])


@router.post("/validation", response_model=NfseQueryResponse)
@limiter.limit("30/minute")
async def validate_nfse(request: Request, payload: NfseQueryRequest) -> NfseQueryResponse:
    return await fetch_nfse_data(payload)
