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
    # Configura o banco de dados criando as tabelas necessárias
    criar_tabelas()

    # Cria a pasta de saída para armazenar os arquivos gerados
    criar_pasta_saida()

    # Raspa os links para os arquivos PDF a partir da URL
    links_pdf = raspar_links_pdf(URL)

    # Faz o download dos PDFs se houver links disponíveis; se não, emite um aviso
    if links_pdf:
        baixar_arquivos_em_paralelo(links_pdf)
    else:
        logging.warning("Nenhum link para PDF encontrado. Nada para baixar.")

    # Compacta os PDFs baixados em um único arquivo ZIP
    compactar_pdfs()

    # Define o caminho do PDF específico a ser processado para extração dos dados
    pdf_path = os.path.join("anexos", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")

    # Extrai os dados do PDF e gera um CSV; se a extração falhar, o fluxo é interrompido
    csv_extraido = extrair_dados(pdf_path)
    if not csv_extraido:
        return

    # Transforma os dados extraídos aplicando as substituições necessárias
    csv_transformado = transformar_dados(csv_extraido)

    # Compacta o CSV final após a transformação
    compactar_csv(csv_transformado)

    # Importa os dados transformados para o banco de dados
    importar_dados()

    # Executa a análise dos dados importados
    analisar_dados()

if __name__ == "__main__":
    main()
