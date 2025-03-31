import os
import csv
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from src import extraction


def test_criar_pasta_saida(tmp_path, monkeypatch):
    fake_saida = tmp_path / "saida"
    monkeypatch.setattr(extraction, "PASTA_SAIDA", str(fake_saida))
    extraction.criar_pasta_saida()
    assert fake_saida.exists()


class FakePdf:
    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, tb):
        pass


def fake_pdf_with_pages():
    fake_page = MagicMock()
    fake_page.extract_tables.return_value = [[["col1", "col2"], ["dado1", "dado2"]]]
    return FakePdf([fake_page])


@patch("src.extraction.pdfplumber.open", return_value=fake_pdf_with_pages())
def test_validar_pdf_valid(mock_pdf_open, tmp_path):
    fake_pdf_path = str(tmp_path / "fake.pdf")
    open(fake_pdf_path, "w").close()
    assert extraction.validar_pdf(fake_pdf_path) is True


def test_processar_pdf(tmp_path):
    fake_csv = StringIO()
    writer = csv.writer(fake_csv)
    fake_pdf_obj = fake_pdf_with_pages()
    with patch("src.extraction.pdfplumber.open", return_value=fake_pdf_obj):
        extraction.processar_pdf("dummy.pdf", writer)
    output = fake_csv.getvalue()
    assert "dado1" in output
    assert "dado2" in output


def test_extrair_dados(monkeypatch, tmp_path):
    from src import extraction

    fake_saida = tmp_path / "saida"
    fake_saida.mkdir()
    monkeypatch.setattr(extraction, "PASTA_SAIDA", str(fake_saida))
    # Simula as funções auxiliares para impedir ações reais
    monkeypatch.setattr(extraction, "criar_pasta_saida", lambda: None)
    monkeypatch.setattr(extraction, "processar_pdf", lambda pdf, writer: None)
    monkeypatch.setattr(extraction, "validar_pdf", lambda pdf: True)
    fake_pdf_path = str(tmp_path / "fake.pdf")
    open(fake_pdf_path, "w").close()
    result = extraction.extrair_dados(fake_pdf_path)
    assert result is not None
    assert result.endswith("dados_extraidos.csv")
