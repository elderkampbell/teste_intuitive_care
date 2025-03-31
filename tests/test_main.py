import os
from unittest.mock import patch
import src.main as main


def test_main_flow():
    with patch("src.main.criar_tabelas") as mock_criar_tabelas, patch(
        "src.main.criar_pasta_saida"
    ) as mock_criar_saida, patch(
        "src.main.raspar_links_pdf", return_value=["link1.pdf"]
    ), patch(
        "src.main.baixar_arquivos_em_paralelo"
    ) as mock_baixar_paralelo, patch(
        "src.main.compactar_pdfs"
    ) as mock_compactar_pdfs, patch(
        "src.main.extrair_dados", return_value="dummy.csv"
    ) as mock_extrair, patch(
        "src.main.transformar_dados", return_value="dummy_transformado.csv"
    ) as mock_transform, patch(
        "src.main.compactar_csv"
    ) as mock_compactar_csv, patch(
        "src.main.importar_dados"
    ) as mock_importar, patch(
        "src.main.analisar_dados"
    ) as mock_analisar:
        main.main()
        mock_criar_tabelas.assert_called_once()
        mock_criar_saida.assert_called_once()
        mock_baixar_paralelo.assert_called_once()
        mock_compactar_pdfs.assert_called_once()
        mock_extrair.assert_called_once()
        mock_transform.assert_called_once()
        mock_compactar_csv.assert_called_once()
        mock_importar.assert_called_once()
        mock_analisar.assert_called_once()
