import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from src.data_analysis import executar_query, main


class FakeCursor:
    def __init__(self):
        self.result = [
            ("operadora1", 1000.50, "2025-01", "2025-03", "Evento1,Evento2"),
            ("operadora2", 800.75, "2025-01", "2025-03", "Evento3"),
        ]

    def execute(self, query):
        pass

    def fetchall(self):
        return self.result

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def commit(self):
        pass

    def close(self):
        pass


@patch("src.data_analysis.conectar_bd", return_value=FakeConnection())
def test_executar_query(mock_conectar, capsys):
    executar_query("SELECT 1", "Teste Query")
    captured = capsys.readouterr().out
    assert "Teste Query" in captured
    assert "Operadora com a maior despesa" in captured


@patch("src.data_analysis.conectar_bd", return_value=FakeConnection())
def test_main(mock_conectar, capsys):
    main()
    captured = capsys.readouterr().out
    assert "Top 10 Operadoras com Maiores Despesas" in captured
