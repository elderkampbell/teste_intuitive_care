import os
from src.parallel import baixar_arquivos_em_paralelo


def test_baixar_arquivos_em_paralelo(mocker):
    """
    Testa o download paralelo de vários arquivos.

    Utiliza o pytest e o mocker para simular o comportamento da função de download.
    """
    # Mock do conteúdo do arquivo para evitar downloads reais
    mock_baixar_arquivo = mocker.patch("src.parallel.baixar_arquivo", return_value=None)

    # Lista de links para arquivos PDF a serem baixados
    links = [
        "https://www.exemplo.com/arquivo1.pdf",
        "https://www.exemplo.com/arquivo2.pdf",
    ]

    # Chama a função que realiza o download em paralelo
    baixar_arquivos_em_paralelo(links)

    # Verifica se a função de download foi chamada para cada link
    for link in links:
        nome_arquivo = os.path.basename(link)  # Extrai o nome do arquivo do link
        # Verifica se a função mockada foi chamada com o link correto e o caminho de saída
        mock_baixar_arquivo.assert_any_call(link, os.path.join("anexos", nome_arquivo))

    # Verifica se a função de download foi chamada o número correto de vezes
    assert mock_baixar_arquivo.call_count == len(links)
