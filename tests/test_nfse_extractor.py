from bot.nfse_extractor import extract_nfse_data


def _load_data(fixtures_dir):
    xml_text = (fixtures_dir / "nfse.xml").read_text(encoding="utf-8")
    html_text = (fixtures_dir / "exibicao_nfse.html").read_text(encoding="utf-8")
    return extract_nfse_data(xml_text, html_text)


def test_extract_nfse_data_core_fields(fixtures_dir):
    data = _load_data(fixtures_dir)

    assert data.nfse_number == "202500000000999"
    assert data.verification_code == "aaaa1111"
    assert data.provider_company_name == "EMPRESA EXEMPLO SERVICOS MEDICOS LTDA"
    assert data.provider_cnpj == "12345678000199"
    assert data.taker_company_name == "Fulano de Tal"
    assert data.taker_document == "11122233344"
    assert data.service_value == "350.00"
    assert data.net_value == "350.00"


def test_extract_nfse_data_absent_optional_fields_are_none(fixtures_dir):
    data = _load_data(fixtures_dir)

    # esta nota nao inclui esses elementos opcionais no XML
    assert data.rps_number is None
    assert data.provider_phone is None
    assert data.taker_email is None
    assert data.deductions_value is None


def test_extract_nfse_data_html_only_descriptions(fixtures_dir):
    data = _load_data(fixtures_dir)

    assert data.service_item_description == "Medicina e biomedicina."
    assert data.tax_code_description == "Medicina"
    assert data.operation_nature_description == "Tributação no município"
    assert data.service_municipality_name == "Belo Horizonte"
