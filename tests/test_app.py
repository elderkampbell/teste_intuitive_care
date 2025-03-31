import json
import pytest
from unittest.mock import patch, MagicMock
from src.app import app, conectar_banco


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Classes falsas para simular conexão com o banco e cursor
class FakeCursor:
    def __init__(self):
        self.result = [
            {
                "id": 1,
                "Registro_ANS": "123",
                "CNPJ": "000",
                "Razao_Social": "Operadora 1",
                "Nome_Fantasia": "Operadora A",
                "UF": "SP",
                "Endereco_eletronico": "email@example.com",
            }
        ]

    def execute(self, query, params=None):
        if query.strip().lower().startswith("select"):
            self.result  # mantém o resultado fixo
        return

    def fetchall(self):
        return self.result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def commit(self):
        pass

    def close(self):
        pass


@patch("src.app.conectar_banco")
def test_buscar_operadoras_sucesso(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "Registro_ANS": "12345",
            "CNPJ": "00.000.000/0000-00",
            "Razao_Social": "Operadora Teste",
            "Nome_Fantasia": "Teste",
            "UF": "SP",
            "Endereco_eletronico": "teste@teste.com",
        }
    ]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    response = client.get("/buscar_operadoras?termo=teste")
    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "Registro_ANS": "12345",
            "CNPJ": "00.000.000/0000-00",
            "Razao_Social": "Operadora Teste",
            "Nome_Fantasia": "Teste",
            "UF": "SP",
            "Endereco_eletronico": "teste@teste.com",
        }
    ]


@patch("src.app.conectar_banco")
def test_buscar_operadoras_erro_conexao(mock_conectar_banco, client):
    mock_conectar_banco.return_value = None

    response = client.get("/buscar_operadoras?termo=teste")
    assert response.status_code == 500
    assert response.json == {"erro": "Erro ao conectar com o banco de dados."}


@patch("src.app.conectar_banco")
def test_adicionar_operadora_sucesso(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    dados = {
        "Registro_ANS": "12345",
        "CNPJ": "00.000.000/0000-00",
        "Razao_Social": "Operadora Teste",
        "Nome_Fantasia": "Teste",
        "Modalidade": "Teste",
        "Logradouro": "Rua Teste",
        "Numero": "123",
        "Complemento": "Apto 1",
        "Bairro": "Bairro Teste",
        "Cidade": "Cidade Teste",
        "UF": "SP",
        "CEP": "00000-000",
        "DDD": "11",
        "Telefone": "123456789",
        "Fax": "987654321",
        "Endereco_eletronico": "teste@teste.com",
        "Representante": "Representante Teste",
        "Cargo_Representante": "Cargo Teste",
        "Regiao_de_Comercializacao": "Região Teste",
        "Data_Registro_ANS": "2023-01-01",
    }

    response = client.post("/operadoras", json=dados)
    assert response.status_code == 201
    assert response.json == {"mensagem": "Operadora adicionada com sucesso!"}


@patch("src.app.conectar_banco")
def test_adicionar_operadora_erro_conexao(mock_conectar_banco, client):
    mock_conectar_banco.return_value = None

    dados = {
        "Registro_ANS": "12345",
        "CNPJ": "00.000.000/0000-00",
        "Razao_Social": "Operadora Teste",
        "Nome_Fantasia": "Teste",
    }

    response = client.post("/operadoras", json=dados)
    assert response.status_code == 500
    assert response.json == {"erro": "Erro ao conectar com o banco de dados."}


@patch("src.app.conectar_banco")
def test_atualizar_operadora_sucesso(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    dados = {"Nome_Fantasia": "Teste Atualizado"}

    response = client.put("/operadoras/1", json=dados)
    assert response.status_code == 200
    assert response.json == {"mensagem": "Operadora atualizada com sucesso!"}


@patch("src.app.conectar_banco")
def test_deletar_operadora_sucesso(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    response = client.delete("/operadoras/1")
    assert response.status_code == 200
    assert response.json == {"mensagem": "Operadora deletada com sucesso!"}
