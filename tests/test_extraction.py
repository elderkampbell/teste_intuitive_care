import os
import csv
import pytest  # type: ignore
from unittest.mock import MagicMock
from src.extraction import extrair_dados

PASTA_ANEXOS = "anexos"
PASTA_SAIDA = "saida"


def test_extrair_dados(mocker):
    """
    Testa se a função `extrair_dados` cria um CSV corretamente a partir do PDF mockado.
    """
    # Mock da estrutura de um PDF com tabela
    mock_page = MagicMock()
    mock_page.extract_tables.return_value = [
        [
            [
                "Procedimento",
                "RN",
                "Vigência",
                "OD",
                "AMB",
                "HCO",
                "HSO",
                "REF",
                "PAC",
                "DUT",
            ],  # Cabeçalho da tabela
            [
                "Consulta Odontológica",
                "541/2022",
                "01/08/2022",
                "OD",
                "AMB",
                "",
                "",
                "",
                "",
                "",
            ],
        ]  # Linha de dados simulada
    ]

    # Mock do PDF
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page]

    # Simula o comportamento do `pdfplumber.open`
    mocker.patch("pdfplumber.open", return_value=mock_pdf)

    # Cria diretórios temporários simulados
    os.makedirs(PASTA_ANEXOS, exist_ok=True)

    # Chama a função
    csv_path = extrair_dados()

    # Verifica se o arquivo foi gerado
    assert os.path.exists(csv_path), "O CSV não foi gerado."

    # Lê o conteúdo do CSV para validação
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    print("\nDEBUG: Cabeçalho do CSV ->", rows[0])
    print(
        "\nDEBUG: Dados extraídos do CSV ->",
        rows[1:] if len(rows) > 1 else "Nenhuma linha de dados",
    )

    # Verifica se há cabeçalho e uma linha de dados
    assert len(rows) > 1, f"O CSV extraído está vazio. Conteúdo: {rows}"
    assert (
        rows[1][0] == "Consulta Odontológica"
    ), f"Erro na extração dos dados: {rows[1]}"

    # Limpeza
    os.remove(csv_path)
    os.rmdir(PASTA_ANEXOS)
