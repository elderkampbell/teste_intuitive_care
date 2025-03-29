import os
from src.utils import (
    criar_pasta_saida,
    compactar_pdfs,
    obter_hash_arquivo,
    compactar_csv,
)


def test_compactar_pdfs():
    """
    Testa a compactação de arquivos em um ZIP.

    Cria arquivos simulados na pasta 'anexos' e verifica se a compactação gera um arquivo ZIP.
    """
    criar_pasta_saida()

    # Limpa arquivos ZIP existentes antes do teste
    for arq in os.listdir():
        if arq.endswith(".zip"):
            os.remove(arq)

    # Cria arquivos simulados na pasta anexos
    with open("anexos/teste1.pdf", "w") as f:
        f.write("PDF de teste 1")
    with open("anexos/teste2.pdf", "w") as f:
        f.write("PDF de teste 2")

    # Compacta os arquivos
    compactar_pdfs()

    # Verifica se o arquivo ZIP foi criado
    arquivos_zip = [arq for arq in os.listdir() if arq.endswith(".zip")]
    assert len(arquivos_zip) == 1  # Deve existir exatamente 1 arquivo ZIP

    # Remove os arquivos criados
    for arq in arquivos_zip:
        os.remove(arq)  # Remove o arquivo ZIP criado

    # Remove os arquivos PDF de teste
    os.remove("anexos/teste1.pdf")
    os.remove("anexos/teste2.pdf")

    # Remove todos os arquivos na pasta 'anexos' antes de removê-la
    for arq in os.listdir("anexos"):
        os.remove(os.path.join("anexos", arq))

    # Remove a pasta 'anexos'
    os.rmdir("anexos")

    PASTA_SAIDA = "saida"


def test_compactar_csv():
    """
    Testa se a compactação do CSV gera um arquivo ZIP corretamente.
    """
    PASTA_SAIDA = "saida"
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Criamos um CSV temporário para o teste
    csv_path = os.path.join(PASTA_SAIDA, "teste.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("coluna1,coluna2\nvalor1,valor2")

    # Executa a compactação
    zip_path = compactar_csv(csv_path)

    # Verifica se o arquivo ZIP foi criado
    assert os.path.exists(zip_path), "O arquivo ZIP não foi gerado."

    # Limpeza manual
    os.remove(csv_path)
    os.remove(zip_path)

    # Remove todos os arquivos restantes antes de excluir a pasta
    for arquivo in os.listdir(PASTA_SAIDA):
        os.remove(os.path.join(PASTA_SAIDA, arquivo))

    os.rmdir(PASTA_SAIDA)
