import os
import logging
import csv
import pdfplumber  # type: ignore

# Configuração de logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Reduz a verbosidade do pdfminer
logging.getLogger("pdfminer").setLevel(logging.WARNING)

# Diretórios para armazenar os arquivos
PASTA_ANEXOS = "anexos"
PASTA_SAIDA = "saida"


def criar_pasta_saida():
    """Cria a pasta de saída para os arquivos processados."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    logging.info(f"Pasta de saída verificada/criada: {PASTA_SAIDA}")


def validar_pdf(pdf_path):
    """Verifica se o PDF é válido antes de processar.

    Args:
        pdf_path (str): Caminho para o arquivo PDF a ser validado.

    Returns:
        bool: True se o PDF é válido e contém páginas, False caso contrário.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return len(pdf.pages) > 0
    except Exception:
        logging.warning(f"PDF inválido ou corrompido: {pdf_path}")
        return False


def processar_pdf(pdf_path, writer):
    """Extrai tabelas do PDF e escreve no CSV.

    Args:
        pdf_path (str): Caminho para o arquivo PDF a ser processado.
        writer (csv.writer): Objeto writer para escrever no arquivo CSV.
    """
    logging.info(f"Processando arquivo PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if not tables:
                    logging.info(f"Nenhuma tabela encontrada na página {page_number}.")
                    continue
                for table in tables:
                    for row in table:
                        if row:
                            # Preenchendo colunas ausentes com strings vazias
                            while len(row) < 10:
                                row.append("")
                            writer.writerow(row)
    except Exception as e:
        logging.error(f"Erro ao processar PDF {pdf_path}: {e}")


def extrair_dados(pdf_path):
    """Executa o processo de extração de tabelas do PDF e salva em CSV.

    Args:
        pdf_path (str): Caminho para o arquivo PDF a ser processado.

    Returns:
        str: Caminho do arquivo CSV gerado, ou None se a extração falhar.
    """
    criar_pasta_saida()  # Cria a pasta de saída se não existir
    csv_path = os.path.join(PASTA_SAIDA, "dados_extraidos.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Escreve o cabeçalho do CSV
        writer.writerow(
            [
                "Procedimento",
                "RN",
                "Vigência",
                "OD",
                "AMB",
                "HCO",
                "HSO",
                "REF",
                "PAC",
                "DUT",
                "SUBGRUPO",
                "GRUPO",
                "CAPITULO",
            ]
        )

        # Valida o PDF antes de processar
        if not validar_pdf(pdf_path):
            logging.error("O PDF fornecido é inválido ou corrompido.")
            return None

        # Processa o PDF e escreve os dados no CSV
        processar_pdf(pdf_path, writer)

    logging.info(f"Extração concluída. Dados salvos em: {csv_path}")
    return csv_path


if __name__ == "__main__":
    # Define o caminho do PDF a ser processado
    pdf_path = os.path.join(PASTA_ANEXOS, "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
    extrair_dados(pdf_path)  # Inicia o processo de extração
