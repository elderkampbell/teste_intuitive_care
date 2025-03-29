import os
import logging
from .utils import criar_pasta_saida, compactar_pdfs, compactar_csv
from .scraping import raspar_links_pdf
from .parallel import baixar_arquivos_em_paralelo
from .extraction import extrair_dados
from .transform import transformar_dados
from .database_setup import criar_tabelas
from .database_import import importar_dados
from .data_analysis import main as analisar_dados

# URL da página que contém os links para os PDFs
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


def main():
    """
    Função principal que executa o fluxo completo:
    1. Criação de uma pasta para saída dos arquivos.
    2. Configuração do banco de dados.
    3. Raspagem dos links para arquivos PDF a partir da URL especificada.
    4. Download dos arquivos PDF encontrados (se houver).
    5. Compactação dos arquivos PDF baixados.
    6. Extração de dados dos PDFs baixados.
    7. Transformação dos dados extraídos.
    8. Compactação do CSV final.
    9. Importação dos dados para o banco.
    """

    # Cria as tabelas no banco de dados
    criar_tabelas()

    # Cria uma pasta para armazenar os arquivos de saída
    criar_pasta_saida()

    # Raspagem dos links para PDFs a partir da URL
    links_pdf = raspar_links_pdf(URL)

    # Verifica se foram encontrados links para PDFs
    if links_pdf:
        # Se links foram encontrados, baixa os arquivos em paralelo
        baixar_arquivos_em_paralelo(links_pdf)
    else:
        # Se nenhum link foi encontrado, registra um aviso
        logging.warning("Nenhum link para PDF encontrado. Nada para baixar.")

    # Compacta os PDFs baixados
    compactar_pdfs()

    # Define o caminho do PDF específico a ser processado
    pdf_path = os.path.join("anexos", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")

    # Extrai dados do PDF especificado
    csv_extraido = extrair_dados(pdf_path)

    # Verifica se a extração foi bem-sucedida
    if not csv_extraido:
        return  # Se não houver dados extraídos, encerra a função

    # Transforma os dados extraídos (substitui abreviações, etc.)
    csv_transformado = transformar_dados(csv_extraido)

    # Compacta o CSV final após a transformação
    compactar_csv(csv_transformado)

    # Importa os dados no banco de dados
    importar_dados()

    # Executa a análise dos dados importados
    analisar_dados()


# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
