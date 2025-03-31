import os
import hashlib
import zipfile
import tempfile
from src.utils import (
    criar_pasta_saida,
    obter_hash_arquivo,
    compactar_pdfs,
    compactar_csv,
)


def test_criar_pasta_saida(tmp_path, monkeypatch):
    fake_dir = tmp_path / "anexos"
    monkeypatch.setattr("src.utils.PASTA_SAIDA", str(fake_dir))
    if fake_dir.exists():
        for root, dirs, files in os.walk(str(fake_dir), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
    criar_pasta_saida()
    assert fake_dir.exists()


def test_obter_hash_arquivo(tmp_path):
    file_path = tmp_path / "teste.txt"
    conteudo = b"conteudo de teste"
    with open(file_path, "wb") as f:
        f.write(conteudo)
    esperado = hashlib.md5(conteudo).hexdigest()
    resultado = obter_hash_arquivo(str(file_path))
    assert resultado == esperado


def test_compactar_pdfs(tmp_path, monkeypatch):
    fake_dir = tmp_path / "anexos"
    fake_dir.mkdir()
    arquivo_teste = fake_dir / "teste.pdf"
    arquivo_teste.write_text("conteudo pdf")
    monkeypatch.setattr("src.utils.PASTA_SAIDA", str(fake_dir))
    compactar_pdfs()
    zip_files = [
        f for f in os.listdir(".") if f.startswith("anexos_") and f.endswith(".zip")
    ]
    assert len(zip_files) > 0
    for f in zip_files:
        os.remove(f)


def test_compactar_csv(tmp_path, monkeypatch):
    fake_dir = tmp_path / "anexos"
    fake_dir.mkdir()
    csv_path = fake_dir / "dados.csv"
    csv_path.write_text("col1,col2\nvalor1,valor2")
    monkeypatch.setattr("src.utils.PASTA_SAIDA", str(fake_dir))
    zip_result = compactar_csv(str(csv_path))
    assert os.path.exists(zip_result)
    with zipfile.ZipFile(zip_result, "r") as zf:
        assert "dados.csv" in zf.namelist()
