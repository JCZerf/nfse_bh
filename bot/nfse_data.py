from dataclasses import dataclass, field

XML_NS = {"n": "http://www.abrasf.org.br/nfse.xsd"}


@dataclass
class NfseData:
    nfse_number: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Numero"},
    )
    verification_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:CodigoVerificacao"},
    )
    issue_date: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:DataEmissao"},
    )
    competence_date: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Competencia"},
    )
    rps_number: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Numero"},
    )
    rps_series: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Serie"},
    )
    rps_type: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Tipo"},
    )

    service_description: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Discriminacao"},
    )
    service_item_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:ItemListaServico"},
    )
    service_item_description: str | None = field(
        default=None,
        metadata={"origin": "html", "path": "Subitem Lista de Serviços LC 116/03 / Descrição:"},
    )
    tax_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:CodigoTributacaoMunicipio"},
    )
    tax_code_description: str | None = field(
        default=None,
        metadata={"origin": "html", "path": "Código de Tributação do Município (CTISS)"},
    )
    operation_nature_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:NaturezaOperacao"},
    )
    operation_nature_description: str | None = field(
        default=None,
        metadata={"origin": "html", "path": "Natureza da Operação:"},
    )
    service_municipality_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:CodigoMunicipio"},
    )
    service_municipality_name: str | None = field(
        default=None,
        metadata={"origin": "html", "path": "Cod/Município da incidência do ISSQN:"},
    )

    service_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorServicos"},
    )
    deductions_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorDeducoes"},
    )
    pis_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorPis"},
    )
    cofins_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorCofins"},
    )
    inss_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorInss"},
    )
    ir_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorIr"},
    )
    csll_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorCsll"},
    )
    iss_withheld_flag: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:IssRetido"},
    )
    iss_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorIss"},
    )
    other_withholdings_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:OutrasRetencoes"},
    )
    calculation_base: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:BaseCalculo"},
    )
    tax_rate: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:Aliquota"},
    )
    net_value: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorLiquidoNfse"},
    )
    unconditional_discount: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:DescontoIncondicionado"},
    )
    conditional_discount: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:DescontoCondicionado"},
    )

    provider_cnpj: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:IdentificacaoPrestador/n:Cnpj"},
    )
    provider_municipal_registration: str | None = field(
        default=None,
        metadata={
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:IdentificacaoPrestador/n:InscricaoMunicipal",
        },
    )
    provider_company_name: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:RazaoSocial"},
    )
    provider_trade_name: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:NomeFantasia"},
    )
    provider_address: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Endereco"},
    )
    provider_address_number: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Numero"},
    )
    provider_neighborhood: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Bairro"},
    )
    provider_municipality_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:CodigoMunicipio"},
    )
    provider_state: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Uf"},
    )
    provider_zip_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Cep"},
    )
    provider_phone: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Contato/n:Telefone"},
    )
    provider_email: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Contato/n:Email"},
    )

    taker_document: str | None = field(
        default=None,
        metadata={
            # CpfCnpj tem um unico filho, Cnpj ou Cpf dependendo do tomador
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:IdentificacaoTomador/n:CpfCnpj",
        },
    )
    taker_municipal_registration: str | None = field(
        default=None,
        metadata={
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:IdentificacaoTomador/n:InscricaoMunicipal",
        },
    )
    taker_company_name: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:RazaoSocial"},
    )
    taker_address: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Endereco"},
    )
    taker_address_number: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Numero"},
    )
    taker_neighborhood: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Bairro"},
    )
    taker_municipality_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:CodigoMunicipio"},
    )
    taker_state: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Uf"},
    )
    taker_zip_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Cep"},
    )
    taker_email: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Contato/n:Email"},
    )

    issuing_municipality_code: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:OrgaoGerador/n:CodigoMunicipio"},
    )
    issuing_state: str | None = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:OrgaoGerador/n:Uf"},
    )
