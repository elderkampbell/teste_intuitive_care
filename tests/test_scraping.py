import os
from src.scraping import raspar_links_pdf, baixar_arquivo


def test_raspar_links_pdf(mocker):
    """
    Testa a raspagem de links PDF.

    Utiliza o pytest e o mocker para simular a resposta da requisição HTTP.
    """
    # Mock da página HTML com links PDF
    html_mock = """
    <html>
        <body>
            <a href="/docs/Anexo1.pdf">Anexo</a>
            <a href="/docs/Anexo2.pdf">Anexo</a>
        </body>
    </html>
    """

    # Mock da requisição GET para retornar o HTML simulado
    mocker.patch(
        "src.scraping.session.get",
        return_value=mocker.Mock(text=html_mock, status_code=200),
    )

    # Chama a função para raspar os links PDF
    links = raspar_links_pdf("https://www.exemplo.com")

    # Verifica se ambos os links foram raspados corretamente
    assert len(links) == 2
    assert "/docs/Anexo1.pdf" in links  # Verifica se o primeiro link está presente
    assert "/docs/Anexo2.pdf" in links  # Verifica se o segundo link está presente


def test_baixar_arquivo(mocker):
    """
    Testa o download de arquivos.

    Utiliza o pytest e o mocker para simular a resposta da requisição HTTP e verificar a criação do arquivo.
    """
    # Mock do conteúdo do arquivo
    mocker.patch(
        "src.scraping.session.get",
        return_value=mocker.Mock(
            content="Conteúdo de teste".encode("utf-8"), status_code=200
        ),
    )

    nome_arquivo = "teste_download.pdf"

    # Chama a função para baixar o arquivo
    baixar_arquivo("https://www.exemplo.com/arquivo.pdf", nome_arquivo)

    # Verifica se o arquivo foi criado
    assert os.path.exists(nome_arquivo)

    # Verifica se o conteúdo do arquivo está correto
    with open(nome_arquivo, "rb") as f:
        assert f.read() == "Conteúdo de teste".encode("utf-8")

    # Limpa após o teste removendo o arquivo criado
    os.remove(nome_arquivo)
