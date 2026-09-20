import base64
import dataclasses
import time
import uuid
from datetime import UTC, datetime

import httpx
from fastapi import HTTPException

from api.core.metrics import (
    captcha_result_total,
    captcha_solve_duration_seconds,
    nfse_queries_total,
    nfse_query_duration_seconds,
)
from api.models.nfse import (
    ExtractedField,
    NfseQueryRequest,
    NfseQueryResponse,
    QueryMetadata,
    SourceData,
)
from bot.bhiss_collector import EXIBICAO_PAGE_URL, check_source_errors, download_nfse_xml, query_nfse
from bot.nfse_extractor import extract_nfse_data

SOURCE_NAME = "BHISS Digital"

SOURCE_ERROR_STATUS_CODES = {
    "not_found": 404,
    "missing_field": 422,
    "captcha_rejected": 502,
    "session_expired": 502,
    "source_unexpected_error": 502,
}

CAPTCHA_RESULT_UNKNOWN_STATUSES = {"source_unexpected_error"}


async def fetch_nfse_data(payload: NfseQueryRequest) -> NfseQueryResponse:
    request_id = uuid.uuid4().hex[:8]
    started_at = time.perf_counter()

    try:
        response = await _query_and_extract(payload, request_id)
    except HTTPException:
        nfse_queries_total.labels(status="failed").inc()
        raise
    except Exception:
        nfse_queries_total.labels(status="error").inc()
        raise
    else:
        nfse_queries_total.labels(status="success").inc()
        return response
    finally:
        nfse_query_duration_seconds.observe(time.perf_counter() - started_at)


async def _query_and_extract(payload: NfseQueryRequest, request_id: str) -> NfseQueryResponse:
    timestamp = datetime.now(UTC)

    # Client isolado por requisição, de propósito: a sessão JSF do BHISS é
    # amarrada ao cookie jar, e compartilhar um client entre consultas
    # concorrentes corrompe a sessão de ambas (confirmado contra o site
    # real). O client compartilhado em api/core/http_client.py existe só
    # para o /health, que faz uma única chamada stateless.
    async with httpx.AsyncClient() as client:
        query_result = await query_nfse(
            client,
            payload.provider_cnpj,
            payload.nfse_number,
            payload.verification_code,
            request_id,
        )
        captcha_solve_duration_seconds.observe(query_result.captcha_duration_seconds)
        exibicao_html = query_result.response.text

        source_error = check_source_errors(exibicao_html)
        if source_error is not None:
            status, message = source_error
            if status not in CAPTCHA_RESULT_UNKNOWN_STATUSES:
                captcha_result_total.labels(
                    result="rejected" if status == "captcha_rejected" else "accepted"
                ).inc()
            raise HTTPException(
                status_code=SOURCE_ERROR_STATUS_CODES.get(status, 502),
                detail={"source": SOURCE_NAME, "message": message},
            )
        captcha_result_total.labels(result="accepted").inc()

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
            source_data=SourceData(
                source=SOURCE_NAME,
                source_url=EXIBICAO_PAGE_URL,
                fields=fields,
                xml_base64=xml_base64,
            ),
        )
    )
