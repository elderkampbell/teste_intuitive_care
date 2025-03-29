import os
import logging
import requests  # type: ignore
from parsel import Selector  # type: ignore

# Cria uma sessão persistente para realizar requisições HTTP
session = requests.Session()


def raspar_links_pdf(url):
    """
    Raspa os links únicos dos arquivos PDF na página especificada.

    Parâmetros:
    url (str): A URL da página a ser raspada.

    Retorna:
    list: Uma lista de links únicos para arquivos PDF encontrados na página.
    """
    try:
        # Faz uma requisição GET para a URL especificada
        resposta = session.get(url, timeout=10)
        resposta.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Cria um seletor para analisar o conteúdo HTML da resposta
        seletor = Selector(text=resposta.text)

        # Extrai links únicos para PDFs que contêm "Anexo" no texto do link
        links_pdf = {
            link.attrib["href"]
            for link in seletor.css("a[href]")
            if "Anexo" in link.css("::text").get()
            and link.attrib["href"].endswith(".pdf")
        }

        logging.info(f"{len(links_pdf)} links únicos para PDFs encontrados.")
        return list(links_pdf)  # Retorna a lista de links, removendo duplicados
    except requests.RequestException:
        logging.exception("Falha ao acessar o site.")
        return []  # Retorna uma lista vazia em caso de erro


def baixar_arquivo(url, caminho_saida):
    """
    Faz o download de um arquivo utilizando uma conexão persistente.

    Parâmetros:
    url (str): A URL do arquivo a ser baixado.
    caminho_saida (str): O caminho onde o arquivo será salvo.
    """
    # Verifica se o arquivo já existe para evitar downloads desnecessários
    if os.path.exists(caminho_saida):
        logging.info(f"O arquivo {caminho_saida} já existe. Pulando download.")
        return

    try:
        # Faz uma requisição GET para a URL do arquivo
        resposta = session.get(url, timeout=10)
        resposta.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Salva o conteúdo do arquivo no caminho especificado
        with open(caminho_saida, "wb") as arquivo:
            arquivo.write(resposta.content)
        logging.info(f"Arquivo salvo: {caminho_saida}")
    except requests.RequestException:
        logging.exception(f"Falha ao baixar o arquivo: {url}")
