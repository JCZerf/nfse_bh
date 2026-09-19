from dataclasses import dataclass, field
from typing import Optional

XML_NS = {"n": "http://www.abrasf.org.br/nfse.xsd"}


@dataclass
class NfseData:
    # Nota
    nfse_number: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Numero"},
    )
    verification_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:CodigoVerificacao"},
    )
    issue_date: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:DataEmissao"},
    )
    competence_date: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Competencia"},
    )
    rps_number: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Numero"},
    )
    rps_series: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Serie"},
    )
    rps_type: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:IdentificacaoRps/n:Tipo"},
    )

    # Servico
    service_description: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Discriminacao"},
    )
    service_item_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:ItemListaServico"},
    )
    service_item_description: Optional[str] = field(
        default=None,
        metadata={"origin": "html", "path": "Subitem Lista de Serviços LC 116/03 / Descrição:"},
    )
    tax_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:CodigoTributacaoMunicipio"},
    )
    tax_code_description: Optional[str] = field(
        default=None,
        metadata={"origin": "html", "path": "Código de Tributação do Município (CTISS)"},
    )
    operation_nature_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:NaturezaOperacao"},
    )
    operation_nature_description: Optional[str] = field(
        default=None,
        metadata={"origin": "html", "path": "Natureza da Operação:"},
    )
    service_municipality_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:CodigoMunicipio"},
    )
    service_municipality_name: Optional[str] = field(
        default=None,
        metadata={"origin": "html", "path": "Cod/Município da incidência do ISSQN:"},
    )

    # Valores
    service_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorServicos"},
    )
    deductions_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorDeducoes"},
    )
    pis_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorPis"},
    )
    cofins_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorCofins"},
    )
    inss_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorInss"},
    )
    ir_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorIr"},
    )
    csll_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorCsll"},
    )
    iss_withheld_flag: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:IssRetido"},
    )
    iss_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorIss"},
    )
    other_withholdings_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:OutrasRetencoes"},
    )
    calculation_base: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:BaseCalculo"},
    )
    tax_rate: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:Aliquota"},
    )
    net_value: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:ValorLiquidoNfse"},
    )
    unconditional_discount: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:DescontoIncondicionado"},
    )
    conditional_discount: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:Servico/n:Valores/n:DescontoCondicionado"},
    )

    # Prestador
    provider_cnpj: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:IdentificacaoPrestador/n:Cnpj"},
    )
    provider_municipal_registration: Optional[str] = field(
        default=None,
        metadata={
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:IdentificacaoPrestador/n:InscricaoMunicipal",
        },
    )
    provider_company_name: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:RazaoSocial"},
    )
    provider_trade_name: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:NomeFantasia"},
    )
    provider_address: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Endereco"},
    )
    provider_address_number: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Numero"},
    )
    provider_neighborhood: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Bairro"},
    )
    provider_municipality_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:CodigoMunicipio"},
    )
    provider_state: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Uf"},
    )
    provider_zip_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Endereco/n:Cep"},
    )
    provider_phone: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Contato/n:Telefone"},
    )
    provider_email: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:PrestadorServico/n:Contato/n:Email"},
    )

    # Tomador
    taker_document: Optional[str] = field(
        default=None,
        metadata={
            # CpfCnpj tem um unico filho, Cnpj ou Cpf dependendo do tomador
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:IdentificacaoTomador/n:CpfCnpj",
        },
    )
    taker_municipal_registration: Optional[str] = field(
        default=None,
        metadata={
            "origin": "xml",
            "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:IdentificacaoTomador/n:InscricaoMunicipal",
        },
    )
    taker_company_name: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:RazaoSocial"},
    )
    taker_address: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Endereco"},
    )
    taker_address_number: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Numero"},
    )
    taker_neighborhood: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Bairro"},
    )
    taker_municipality_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:CodigoMunicipio"},
    )
    taker_state: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Uf"},
    )
    taker_zip_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Endereco/n:Cep"},
    )
    taker_email: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:TomadorServico/n:Contato/n:Email"},
    )

    # Orgao gerador
    issuing_municipality_code: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:OrgaoGerador/n:CodigoMunicipio"},
    )
    issuing_state: Optional[str] = field(
        default=None,
        metadata={"origin": "xml", "path": "n:Nfse/n:InfNfse/n:OrgaoGerador/n:Uf"},
    )
