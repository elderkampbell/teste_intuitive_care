import os
from src.parallel import baixar_arquivos_em_paralelo


def test_baixar_arquivos_em_paralelo(mocker):
    mock_baixar_arquivo = mocker.patch("src.parallel.baixar_arquivo", return_value=None)
    links = [
        "https://www.exemplo.com/arquivo1.pdf",
        "https://www.exemplo.com/arquivo2.pdf",
    ]
    baixar_arquivos_em_paralelo(links)
    for link in links:
        nome_arquivo = os.path.basename(link)
        mock_baixar_arquivo.assert_any_call(link, os.path.join("anexos", nome_arquivo))
    assert mock_baixar_arquivo.call_count == len(links)
