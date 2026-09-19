import pytest

from bot.bhiss_collector import extract_download_button_name, extract_view_state


def test_extract_view_state_finds_value(fixtures_dir):
    html = (fixtures_dir / "consulta_page.html").read_text(encoding="utf-8")
    assert extract_view_state(html) == "j_id1"


def test_extract_view_state_missing_raises():
    with pytest.raises(ValueError):
        extract_view_state("<html><body>sem viewstate aqui</body></html>")


def test_extract_download_button_name(fixtures_dir):
    html = (fixtures_dir / "exibicao_nfse.html").read_text(encoding="utf-8")
    assert extract_download_button_name(html) == "form:j_id18"


def test_extract_download_button_name_missing_raises():
    with pytest.raises(ValueError):
        extract_download_button_name("<html><body>sem botao de download</body></html>")
