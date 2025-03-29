import os
import logging
from zipfile import ZipFile
from datetime import datetime
import hashlib

# Configuração do logging para registrar informações e erros
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define o diretório onde os arquivos baixados serão armazenados
PASTA_SAIDA = "anexos"


def criar_pasta_saida():
    """
    Cria a pasta de saída para armazenar os arquivos baixados, caso ela não exista.
    """
    os.makedirs(PASTA_SAIDA, exist_ok=True)  # Cria a pasta, se não existir
    logging.info(f"Pasta de saída configurada: {PASTA_SAIDA}")


def obter_hash_arquivo(caminho):
    """
    Gera um hash MD5 do conteúdo de um arquivo.

    Parâmetros:
    caminho (str): O caminho do arquivo para o qual o hash será gerado.

    Retorna:
    str: O hash MD5 do arquivo.
    """
    hash_md5 = hashlib.md5()  # Cria um objeto hash MD5
    with open(caminho, "rb") as f:  # Abre o arquivo em modo binário
        for chunk in iter(lambda: f.read(4096), b""):  # Lê o arquivo em pedaços
            hash_md5.update(chunk)  # Atualiza o hash com o conteúdo lido
    return hash_md5.hexdigest()  # Retorna o hash em formato hexadecimal


def compactar_pdfs():
    """
    Compacta os arquivos PDFs em um único arquivo ZIP.

    O arquivo ZIP é nomeado com a data e hora atuais.
    """
    # Nome do arquivo ZIP com data e hora
    nome_zip = f"anexos_{datetime.now().strftime('%d%m%Y_%H%M%S')}.zip"
    try:
        # Cria um novo arquivo ZIP
        with ZipFile(nome_zip, "w") as zipf:
            # Percorre a pasta de saída e adiciona os arquivos ao ZIP
            for raiz, _, arquivos in os.walk(PASTA_SAIDA):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(
                        raiz, arquivo
                    )  # Caminho completo do arquivo
                    zipf.write(
                        caminho_completo, arcname=arquivo
                    )  # Adiciona o arquivo ao ZIP
        # Obtém o tamanho do arquivo ZIP em MB
        tamanho_zip = os.path.getsize(nome_zip) / (1024 * 1024)  # Tamanho em MB
        logging.info(
            f"Arquivos compactados em: {nome_zip} (Tamanho: {tamanho_zip:.2f} MB)"
        )
    except Exception:
        logging.exception("Erro ao compactar arquivos.")


def compactar_csv(csv_path):
    """
    Compacta o arquivo CSV em um ZIP.

    Parâmetros:
    csv_path (str): O caminho do arquivo CSV a ser compactado.

    Retorna:
    str: O caminho do arquivo ZIP gerado.
    """
    # Constantes
    NOME_ARQUIVO_FINAL = "Teste_elder_kampbell.zip"  # Nomeia o .zip

    # Define o caminho do arquivo ZIP
    zip_path = os.path.join(PASTA_SAIDA, NOME_ARQUIVO_FINAL)

    try:
        # Cria um novo arquivo ZIP e adiciona o CSV
        with ZipFile(zip_path, "w") as zipf:
            zipf.write(csv_path, arcname=os.path.basename(csv_path))
        logging.info(f"Arquivo ZIP gerado: {zip_path}")
    except Exception:
        logging.exception("Erro ao compactar o arquivo CSV.")

    return zip_path
