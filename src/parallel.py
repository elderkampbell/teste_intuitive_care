import os
from concurrent.futures import ThreadPoolExecutor
from src.scraping import baixar_arquivo

# Diretório onde os arquivos baixados serão salvos
PASTA_SAIDA = "anexos"

def baixar_arquivos_em_paralelo(links):
    # Utiliza ThreadPoolExecutor para realizar múltiplos downloads em paralelo (até 5 threads)
    with ThreadPoolExecutor(max_workers=5) as executor:
        for link in links:
            # Se o link não for uma URL completa, adiciona o prefixo padrão
            url_pdf = link if link.startswith("http") else f"https://www.gov.br{link}"
            # Define o caminho de saída utilizando o diretório PADRAO e o nome do arquivo
            caminho_saida = os.path.join(PASTA_SAIDA, os.path.basename(url_pdf))
            # Agenda a tarefa de download para ser executada em paralelo
            executor.submit(baixar_arquivo, url_pdf, caminho_saida)
