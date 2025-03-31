import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src import database_setup


class FakeCursor:
    def __init__(self):
        self.queries = []

    def execute(self, query, params=None):
        self.queries.append(query)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        pass


class FakeConnection:
    def __init__(self):
        self.fake_cursor = FakeCursor()

    def cursor(self):
        return self.fake_cursor

    def commit(self):
        pass

    def close(self):
        pass


@patch("src.database_setup.mysql.connector.connect", return_value=FakeConnection())
def test_criar_tabelas(mock_connect):
    database_setup.criar_tabelas()


@patch("src.database_setup.requests.get")
@patch("src.database_setup.mysql.connector.connect", return_value=FakeConnection())
@patch(
    "src.database_setup.pd.read_csv",
    return_value=pd.DataFrame(
        {
            "Registro_ANS": ["001"],
            "CNPJ": ["123"],
            "Razao_Social": ["Operadora X"],
            "Nome_Fantasia": ["X"],
            "Modalidade": ["Modal"],
            "UF": ["SP"],
            "municipio": ["Cidade"],
            "Data_Registro_ANS": ["2025-01-01"],
        }
    ),
)
def test_importar_operadoras(mock_read_csv, mock_connect, mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.content = b"conteudo"
    mock_get.return_value = fake_response
    database_setup.importar_operadoras()
    mock_get.assert_called()
