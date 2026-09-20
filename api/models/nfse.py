from datetime import datetime

from pydantic import BaseModel, Field, field_validator

CNPJ_PATTERN = r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$"
NFSE_NUMBER_PATTERN = r"^(\d{1,15}|\d{4}/\d{1,11})$"
VERIFICATION_CODE_PATTERN = r"^[0-9a-f]{8}$"


class NfseQueryRequest(BaseModel):
    provider_cnpj: str = Field(pattern=CNPJ_PATTERN)
    nfse_number: str = Field(pattern=NFSE_NUMBER_PATTERN)
    verification_code: str = Field(pattern=VERIFICATION_CODE_PATTERN)

    @field_validator("provider_cnpj")
    @classmethod
    def normalize_provider_cnpj(cls, value: str) -> str:
        digits = "".join(char for char in value if char.isdigit())
        return f"{digits[0:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"

    @field_validator("nfse_number")
    @classmethod
    def normalize_nfse_number(cls, value: str) -> str:
        if "/" not in value:
            return value
        year, sequential = value.split("/", 1)
        return year + sequential.zfill(15 - len(year))


class ExtractedField(BaseModel):
    name: str
    origin: str
    value: str | None


class SourceData(BaseModel):
    source: str
    source_url: str
    fields: list[ExtractedField]
    xml_base64: str


class QueryMetadata(BaseModel):
    request_id: str
    timestamp: datetime
    source_data: SourceData


class NfseQueryResponse(BaseModel):
    metadata: QueryMetadata
