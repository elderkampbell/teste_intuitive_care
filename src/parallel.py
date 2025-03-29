import os
from concurrent.futures import ThreadPoolExecutor
from src.scraping import baixar_arquivo

# Define o diretório onde os arquivos baixados serão armazenados
PASTA_SAIDA = "anexos"


def baixar_arquivos_em_paralelo(links):
    """
    Faz o download de vários arquivos em paralelo.

    Parâmetros:
    links (list): Uma lista de URLs para os arquivos PDF a serem baixados.
    """
    # Cria um executor de threads para realizar downloads em paralelo
    with ThreadPoolExecutor(max_workers=5) as executor:
        for link in links:
            # Verifica se o link é uma URL completa; caso contrário, adiciona o prefixo
            url_pdf = link if link.startswith("http") else f"https://www.gov.br{link}"

            # Define o caminho de saída para o arquivo baixado
            caminho_saida = os.path.join(PASTA_SAIDA, os.path.basename(url_pdf))

            # Envia a tarefa de download para o executor
            executor.submit(baixar_arquivo, url_pdf, caminho_saida)
