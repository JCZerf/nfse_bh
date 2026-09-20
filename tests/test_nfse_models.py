import pytest
from pydantic import ValidationError

from api.models.nfse import NfseQueryRequest


def test_valid_payload_with_formatted_cnpj():
    request = NfseQueryRequest(
        provider_cnpj="35.142.610/0001-04",
        nfse_number="202500000000118",
        verification_code="df092c28",
    )
    assert request.provider_cnpj == "35.142.610/0001-04"


def test_valid_payload_with_unformatted_cnpj():
    request = NfseQueryRequest(
        provider_cnpj="35142610000104",
        nfse_number="118",
        verification_code="aaaa1111",
    )
    assert request.nfse_number == "118"


def test_nfse_number_natural_format_is_normalized_to_canonical():
    request = NfseQueryRequest(
        provider_cnpj="21.150.875/0001-40",
        nfse_number="2020/10823",
        verification_code="a1dd4050",
    )
    assert request.nfse_number == "202000000010823"


def test_nfse_number_canonical_format_is_left_unchanged():
    request = NfseQueryRequest(
        provider_cnpj="35.142.610/0001-04",
        nfse_number="202500000000118",
        verification_code="df092c28",
    )
    assert request.nfse_number == "202500000000118"


@pytest.mark.parametrize(
    "field, value",
    [
        ("provider_cnpj", "string"),
        ("provider_cnpj", "35.142.610/0001-0"),
        ("nfse_number", "string"),
        ("nfse_number", "1" * 16),
        ("nfse_number", "2020/" + "1" * 12),
        ("nfse_number", "20/10823"),
        ("verification_code", "string"),
        ("verification_code", "DF092C28"),
        ("verification_code", "df092c2"),
    ],
)
def test_invalid_fields_are_rejected(field, value):
    payload = {
        "provider_cnpj": "35.142.610/0001-04",
        "nfse_number": "202500000000118",
        "verification_code": "df092c28",
    }
    payload[field] = value

    with pytest.raises(ValidationError):
        NfseQueryRequest(**payload)
