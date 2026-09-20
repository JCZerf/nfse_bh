import pytest

from bot.bhiss_collector import check_source_errors, extract_download_button_name, extract_view_state


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


def test_check_source_errors_returns_none_on_success(fixtures_dir):
    html = (fixtures_dir / "exibicao_nfse.html").read_text(encoding="utf-8")
    assert check_source_errors(html) is None


def test_check_source_errors_session_expired():
    html = "<html><head><title>Sess&atilde;o Expirada</title></head></html>"
    assert check_source_errors(html) == ("session_expired", "Sessao expirada")


def test_check_source_errors_captcha_rejected():
    html = (
        '<li class="mensagenserro">O c&oacute;digo informado referente a '
        "imagem de seguran&ccedil;a est&aacute; incorreto.</li>"
    )
    status, message = check_source_errors(html)
    assert status == "captcha_rejected"
    assert "imagem de segurança" in message


def test_check_source_errors_missing_field():
    html = '<li class="mensagenserro">Campo "N&uacute;mero da NFS-e" &eacute; obrigat&oacute;rio.</li>'
    status, message = check_source_errors(html)
    assert status == "missing_field"
    assert "obrigatório" in message


def test_check_source_errors_not_found():
    html = (
        '<li style="alerta">O sistema n&atilde;o localizou nenhum '
        "registro para esta pesquisa.</li>"
    )
    status, message = check_source_errors(html)
    assert status == "not_found"
    assert "não localizou" in message


def test_check_source_errors_unexpected_source_error():
    html = '<h1>Ocorreu um erro inesperado na aplica&ccedil;&atilde;o. Tente realizar a operacao novamente.</h1>'
    status, message = check_source_errors(html)
    assert status == "source_unexpected_error"
