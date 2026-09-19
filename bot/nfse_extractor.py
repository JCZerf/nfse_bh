import dataclasses
import xml.etree.ElementTree as ElementTree

from bs4 import BeautifulSoup

from .nfse_data import XML_NS, NfseData

CPF_CNPJ_PARENT_PATH = "n:Nfse/n:InfNfse/n:TomadorServico/n:IdentificacaoTomador/n:CpfCnpj"


def _extract_xml_value(root: ElementTree.Element, path: str) -> str | None:
    element = root.find(path, XML_NS)
    if element is None or element.text is None:
        return None
    return element.text.strip()


def _extract_taker_document(root: ElementTree.Element) -> str | None:
    cpf_cnpj = root.find(CPF_CNPJ_PARENT_PATH, XML_NS)
    if cpf_cnpj is None or len(cpf_cnpj) == 0:
        return None
    return (cpf_cnpj[0].text or "").strip() or None


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _extract_html_value(soup: BeautifulSoup, label: str) -> str | None:
    normalized_label = _normalize_whitespace(label)
    label_span = soup.find(
        "span",
        class_="subTitulo",
        string=lambda text: bool(text) and normalized_label in _normalize_whitespace(text),
    )
    if label_span is None:
        return None
    value_paragraph = label_span.find_next("p", class_="teste")
    if value_paragraph is None:
        return None
    value = _normalize_whitespace(value_paragraph.get_text(strip=True))
    return value or None


def _extract_description_after_slash(raw_value: str | None) -> str | None:
    if raw_value is None:
        return None
    if " / " not in raw_value:
        return raw_value
    return raw_value.split(" / ", 1)[1].strip()


def extract_nfse_data(xml_text: str, html_text: str) -> NfseData:
    root = ElementTree.fromstring(xml_text)
    soup = BeautifulSoup(html_text, "html.parser")

    values: dict[str, str | None] = {}
    for data_field in dataclasses.fields(NfseData):
        origin = data_field.metadata["origin"]
        path = data_field.metadata["path"]

        if data_field.name == "taker_document":
            values[data_field.name] = _extract_taker_document(root)
        elif origin == "xml":
            values[data_field.name] = _extract_xml_value(root, path)
        else:
            raw_value = _extract_html_value(soup, path)
            values[data_field.name] = _extract_description_after_slash(raw_value)

    return NfseData(**values)
