import logging
import re
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from captcha_solver.solver import solve as solve_captcha

logger = logging.getLogger(__name__)

BASE_URL = "https://bhissdigital.pbh.gov.br/nfse"
QUERY_PAGE_URL = f"{BASE_URL}/pages/consultaNFS-e_cidadao.jsf"
EXIBICAO_PAGE_URL = f"{BASE_URL}/pages/exibicaoNFS-e.jsf"
CAPTCHA_URL = f"{BASE_URL}/captcha.jpg"

VIEW_STATE_PATTERN = re.compile(
    r'javax\.faces\.ViewState" id="javax\.faces\.ViewState" value="([^"]+)"'
)
DOWNLOAD_BUTTON_PATTERN = re.compile(r'bt_download\.gif" name="(form:[\w-]+)"')

BROWSER_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
    ),
}


async def fetch_query_page(client: httpx.AsyncClient, request_id: str) -> str:
    logger.info("[%s] GET pagina de consulta", request_id)
    response = await client.get(QUERY_PAGE_URL, headers=BROWSER_HEADERS)
    response.raise_for_status()
    return response.text


def extract_view_state(page_html: str) -> str:
    match = VIEW_STATE_PATTERN.search(page_html)
    if match is None:
        raise ValueError("javax.faces.ViewState nao encontrado na pagina de consulta")
    return match.group(1)


async def fetch_captcha(client: httpx.AsyncClient, request_id: str) -> bytes:
    logger.info("[%s] GET captcha", request_id)
    response = await client.get(CAPTCHA_URL, headers=BROWSER_HEADERS)
    response.raise_for_status()
    return response.content


async def query_nfse(
    client: httpx.AsyncClient,
    provider_cnpj: str,
    nfse_number: str,
    verification_code: str,
    request_id: str,
) -> httpx.Response:
    page_html = await fetch_query_page(client, request_id)
    view_state = extract_view_state(page_html)

    captcha_bytes = await fetch_captcha(client, request_id)
    captcha_response = solve_captcha(captcha_bytes, request_id)

    return await submit_query(
        client,
        provider_cnpj,
        nfse_number,
        verification_code,
        captcha_response,
        view_state,
        request_id,
    )


def extract_download_button_name(exibicao_html: str) -> str:
    match = DOWNLOAD_BUTTON_PATTERN.search(exibicao_html)
    if match is None:
        raise ValueError("botao de download nao encontrado na pagina da nota")
    return match.group(1)


async def download_nfse_xml(client: httpx.AsyncClient, exibicao_html: str, request_id: str) -> str:
    view_state = extract_view_state(exibicao_html)
    download_button_name = extract_download_button_name(exibicao_html)

    form_data = {
        "form": "form",
        f"{download_button_name}.x": "10",
        f"{download_button_name}.y": "10",
        "javax.faces.ViewState": view_state,
    }
    headers = {
        **BROWSER_HEADERS,
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://bhissdigital.pbh.gov.br",
        "referer": EXIBICAO_PAGE_URL,
    }
    logger.info("[%s] POST download do xml da nota", request_id)
    response = await client.post(
        EXIBICAO_PAGE_URL,
        data=form_data,
        headers=headers,
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.text


async def submit_query(
    client: httpx.AsyncClient,
    provider_cnpj: str,
    nfse_number: str,
    verification_code: str,
    captcha_response: str,
    view_state: str,
    request_id: str,
) -> httpx.Response:
    form_data = {
        "form": "form",
        "form:cnpjPrestador": provider_cnpj,
        "form:numeroNfsE": nfse_number,
        "form:codVerif": verification_code,
        "j_captcha_response": captcha_response,
        "form:bt_procurar_NFS-e.x": "36",
        "form:bt_procurar_NFS-e.y": "7",
        "javax.faces.ViewState": view_state,
    }
    headers = {
        **BROWSER_HEADERS,
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://bhissdigital.pbh.gov.br",
        "referer": QUERY_PAGE_URL,
    }
    logger.info("[%s] POST consulta da NFS-e", request_id)
    return await client.post(
        QUERY_PAGE_URL,
        data=form_data,
        headers=headers,
        follow_redirects=True,
    )
