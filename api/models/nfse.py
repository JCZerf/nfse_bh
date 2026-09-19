from datetime import datetime

from pydantic import BaseModel, Field

CNPJ_PATTERN = r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$"
NFSE_NUMBER_PATTERN = r"^\d{1,15}$"
VERIFICATION_CODE_PATTERN = r"^[0-9a-f]{8}$"


class NfseQueryRequest(BaseModel):
    provider_cnpj: str = Field(pattern=CNPJ_PATTERN)
    nfse_number: str = Field(pattern=NFSE_NUMBER_PATTERN)
    verification_code: str = Field(pattern=VERIFICATION_CODE_PATTERN)


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
