import os
import logging
import requests  # type: ignore
from parsel import Selector  # type: ignore

# Cria uma sessão persistente para as requisições HTTP
session = requests.Session()

def raspar_links_pdf(url):
    # Realiza uma requisição GET para a URL e valida a resposta
    try:
        resposta = session.get(url, timeout=10)
        resposta.raise_for_status()  # Garante que a requisição foi bem-sucedida

        # Analisa o HTML retornado para extrair os dados desejados
        seletor = Selector(text=resposta.text)

        # Extrai links únicos de arquivos PDF:
        # - Seleciona todos os elementos <a> com atributo "href"
        # - Filtra por links cujo texto contenha "Anexo" e cujo "href" termine com ".pdf"
        links_pdf = {
            link.attrib["href"]
            for link in seletor.css("a[href]")
            if "Anexo" in link.css("::text").get() and link.attrib["href"].endswith(".pdf")
        }

        logging.info(f"{len(links_pdf)} links únicos para PDFs encontrados.")
        return list(links_pdf)  # Retorna a lista de links (removendo duplicados)
    except requests.RequestException:
        logging.exception("Falha ao acessar o site.")
        return []  # Em caso de erro, retorna uma lista vazia

def baixar_arquivo(url, caminho_saida):
    # Checa se o arquivo já existe para evitar downloads desnecessários
    if os.path.exists(caminho_saida):
        logging.info(f"O arquivo {caminho_saida} já existe. Pulando download.")
        return

    try:
        # Faz o download do arquivo via GET request
        resposta = session.get(url, timeout=10)
        resposta.raise_for_status()  # Valida a resposta

        # Salva o conteúdo baixado no caminho especificado
        with open(caminho_saida, "wb") as arquivo:
            arquivo.write(resposta.content)
        logging.info(f"Arquivo salvo: {caminho_saida}")
    except requests.RequestException:
        logging.exception(f"Falha ao baixar o arquivo: {url}")
