import os
import zipfile
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src import database_import
from src.database_import import corrigir_dados


def test_corrigir_dados():
    df = pd.DataFrame(
        {
            "DATA": ["01/01/2025", "15/02/2025"],
            "VL_SALDO_INICIAL": ["1,234", "2,345"],
            "VL_SALDO_FINAL": ["2,345", "3,456"],
        }
    )
    df_corrigido = corrigir_dados(df)
    assert df_corrigido["DATA"].iloc[0] == "2025-01-01"
    assert isinstance(df_corrigido["VL_SALDO_INICIAL"].iloc[0], float)


@patch("src.database_import.os.path.exists", return_value=True)
@patch("src.database_import.requests.get")
def test_baixar_arquivos_existente(mock_get, mock_exists):
    database_import.baixar_arquivos()
    mock_get.assert_not_called()


def test_extrair_zip(tmp_path, monkeypatch):
    downloads = tmp_path / "downloads"
    relatorios = tmp_path / "relatorios"
    downloads.mkdir()
    relatorios.mkdir()
    fake_zip = downloads / "teste.zip"
    with zipfile.ZipFile(fake_zip, "w") as zf:
        zf.writestr("teste.txt", "conteudo")
    monkeypatch.setattr(database_import, "DIRETORIO_ANEXOS", str(downloads))
    monkeypatch.setattr(database_import, "DIRETORIO_EXTRAIDOS", str(relatorios))
    database_import.extrair_zip()
    assert (relatorios / "teste.txt").exists()


class FakeCursor:
    def execute(self, query, params=None):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, typ, val, tb):
        pass


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def commit(self):
        pass

    def close(self):
        pass


@patch("src.database_import.conectar_bd", return_value=FakeConnection())
@patch(
    "src.database_import.pd.read_csv",
    return_value=pd.DataFrame(
        {
            "DATA": ["01/01/2025"],
            "REG_ANS": ["001"],
            "CD_CONTA_CONTABIL": ["123"],
            "DESCRICAO": ["Despesa"],
            "VL_SALDO_INICIAL": ["1,000"],
            "VL_SALDO_FINAL": ["2,000"],
        }
    ),
)
def test_importar_demonstracoes(mock_read_csv, mock_conectar):
    database_import.importar_demonstracoes()
    mock_read_csv.assert_called()


@patch("src.database_import.requests.get")
@patch("src.database_import.conectar_bd", return_value=FakeConnection())
@patch(
    "src.database_import.pd.read_csv",
    return_value=pd.DataFrame(
        {
            "Registro_ANS": ["001"],
            "CNPJ": ["123"],
            "Razao_Social": ["Operadora X"],
            "Nome_Fantasia": ["X"],
            "Modalidade": ["Modal"],
            "Logradouro": ["Rua X"],
            "Numero": ["100"],
            "Complemento": [""],
            "Bairro": ["Centro"],
            "Cidade": ["Cidade"],
            "UF": ["SP"],
            "CEP": ["12345"],
            "DDD": ["11"],
            "Telefone": ["1234"],
            "Fax": ["0000"],
            "Endereco_eletronico": ["x@ex.com"],
            "Representante": ["Rep"],
            "Cargo_Representante": ["Cargo"],
            "Regiao_de_Comercializacao": ["Regiao"],
            "Data_Registro_ANS": ["2025-01-01"],
        }
    ),
)
def test_importar_operadoras(mock_read_csv, mock_conectar, mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.content = b"conteudo"
    mock_get.return_value = fake_response
    database_import.importar_operadoras()
    mock_get.assert_called()
