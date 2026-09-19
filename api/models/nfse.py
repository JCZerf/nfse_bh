from datetime import datetime

from pydantic import BaseModel


class NfseQueryRequest(BaseModel):
    provider_cnpj: str
    nfse_number: str
    verification_code: str


class ExtractedField(BaseModel):
    name: str
    origin: str
    value: str | None


class SourceData(BaseModel):
    fields: list[ExtractedField]
    xml_base64: str


class QueryMetadata(BaseModel):
    request_id: str
    timestamp: datetime
    source_data: SourceData


class NfseQueryResponse(BaseModel):
    metadata: QueryMetadata
