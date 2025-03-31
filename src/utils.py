import os
import logging
from zipfile import ZipFile
from datetime import datetime
import hashlib

# Configura o logging para registrar informações e erros com data/hora e nível da mensagem
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Diretório onde os arquivos (por exemplo, baixados ou gerados) serão armazenados
PASTA_SAIDA = "anexos"

# Cria a pasta de saída se ela ainda não existir e registra a ação
def criar_pasta_saida():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    logging.info(f"Pasta de saída configurada: {PASTA_SAIDA}")

# Gera o hash MD5 de um arquivo, lendo-o em blocos para economizar memória
def obter_hash_arquivo(caminho):
    hash_md5 = hashlib.md5()  # Inicializa o objeto para criar o hash MD5
    with open(caminho, "rb") as f:  # Abre o arquivo em modo binário
        for chunk in iter(lambda: f.read(4096), b""):  # Lê o arquivo em blocos de 4096 bytes
            hash_md5.update(chunk)
    return hash_md5.hexdigest()  # Retorna o hash no formato hexadecimal

# Compacta os arquivos contidos na pasta de saída em um único arquivo ZIP nomeado com data/hora atual
def compactar_pdfs():
    nome_zip = f"anexos_{datetime.now().strftime('%d%m%Y_%H%M%S')}.zip"  # Define o nome do ZIP
    try:
        with ZipFile(nome_zip, "w") as zipf:  # Cria e abre o arquivo ZIP para escrita
            for raiz, _, arquivos in os.walk(PASTA_SAIDA):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(raiz, arquivo)
                    zipf.write(caminho_completo, arcname=arquivo)  # Adiciona cada arquivo ao ZIP
        tamanho_zip = os.path.getsize(nome_zip) / (1024 * 1024)  # Calcula o tamanho do ZIP em MB
        logging.info(f"Arquivos compactados em: {nome_zip} (Tamanho: {tamanho_zip:.2f} MB)")
    except Exception:
        logging.exception("Erro ao compactar arquivos.")

# Compacta um arquivo CSV específico, gerando um ZIP com um nome padrão e retornando seu caminho
def compactar_csv(csv_path):
    NOME_ARQUIVO_FINAL = "Teste_elder_kampbell.zip"  # Nome padrão para o ZIP gerado
    zip_path = os.path.join(PASTA_SAIDA, NOME_ARQUIVO_FINAL)
    try:
        with ZipFile(zip_path, "w") as zipf:
            # Adiciona o CSV ao ZIP, preservando apenas o nome do arquivo
            zipf.write(csv_path, arcname=os.path.basename(csv_path))
        logging.info(f"Arquivo ZIP gerado: {zip_path}")
    except Exception:
        logging.exception("Erro ao compactar o arquivo CSV.")
    return zip_path
