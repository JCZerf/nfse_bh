import base64
import dataclasses
import uuid
from datetime import datetime, timezone

import httpx
from fastapi import HTTPException

from bot.bhiss_collector import download_nfse_xml, query_nfse
from bot.nfse_extractor import extract_nfse_data

from api.models.nfse import (
    ExtractedField,
    NfseQueryRequest,
    NfseQueryResponse,
    QueryMetadata,
    SourceData,
)


async def fetch_nfse_data(payload: NfseQueryRequest) -> NfseQueryResponse:
    request_id = uuid.uuid4().hex[:8]
    timestamp = datetime.now(timezone.utc)

    async with httpx.AsyncClient() as client:
        exibicao_response = await query_nfse(
            client,
            payload.provider_cnpj,
            payload.nfse_number,
            payload.verification_code,
            request_id,
        )
        exibicao_html = exibicao_response.text

        if "exibicaoNFS-e" not in str(exibicao_response.url):
            raise HTTPException(status_code=404, detail="NFS-e nao encontrada")

        xml_text = await download_nfse_xml(client, exibicao_html, request_id)

    nfse_data = extract_nfse_data(xml_text, exibicao_html)
    fields = [
        ExtractedField(
            name=data_field.name,
            origin=data_field.metadata["origin"],
            value=getattr(nfse_data, data_field.name),
        )
        for data_field in dataclasses.fields(nfse_data)
    ]
    xml_base64 = base64.b64encode(xml_text.encode("utf-8")).decode("ascii")

    return NfseQueryResponse(
        metadata=QueryMetadata(
            request_id=request_id,
            timestamp=timestamp,
            source_data=SourceData(fields=fields, xml_base64=xml_base64),
        )
    )
