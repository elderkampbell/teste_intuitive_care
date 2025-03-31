import os
from src.scraping import raspar_links_pdf, baixar_arquivo


def test_raspar_links_pdf(mocker):
    html_mock = """
    <html>
        <body>
            <a href="/docs/Anexo1.pdf">Anexo</a>
            <a href="/docs/Anexo2.pdf">Anexo</a>
        </body>
    </html>
    """
    mocker.patch(
        "src.scraping.session.get",
        return_value=mocker.Mock(text=html_mock, status_code=200),
    )
    links = raspar_links_pdf("https://www.exemplo.com")
    assert len(links) == 2
    assert "/docs/Anexo1.pdf" in links
    assert "/docs/Anexo2.pdf" in links


def test_baixar_arquivo(mocker):
    mocker.patch(
        "src.scraping.session.get",
        return_value=mocker.Mock(
            content="Conteúdo de teste".encode("utf-8"), status_code=200
        ),
    )
    nome_arquivo = "teste_download.pdf"
    baixar_arquivo("https://www.exemplo.com/arquivo.pdf", nome_arquivo)
    assert os.path.exists(nome_arquivo)
    with open(nome_arquivo, "rb") as f:
        assert f.read() == "Conteúdo de teste".encode("utf-8")
    os.remove(nome_arquivo)
