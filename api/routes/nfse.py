from fastapi import APIRouter, Depends

from api.dependencies.auth import verify_api_key
from api.models.nfse import NfseQueryRequest, NfseQueryResponse
from api.services.nfse_service import fetch_nfse_data

router = APIRouter(prefix="/nfse", tags=["nfse"], dependencies=[Depends(verify_api_key)])


@router.post("/validation", response_model=NfseQueryResponse)
async def validate_nfse(payload: NfseQueryRequest) -> NfseQueryResponse:
    return await fetch_nfse_data(payload)
