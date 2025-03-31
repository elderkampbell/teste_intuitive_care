import os
import logging
import csv
import pdfplumber  # type: ignore

# Configura o logging com nível INFO e formatação padrão com data, nível e mensagem.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Reduz a verbosidade das mensagens do pdfminer para evitar logs excessivos.
logging.getLogger("pdfminer").setLevel(logging.WARNING)

# Diretórios usados para armazenar os arquivos de entrada e saída.
PASTA_ANEXOS = "anexos"
PASTA_SAIDA = "saida"


def criar_pasta_saida():
    # Garante que a pasta de saída exista, criando-a se necessário.
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    logging.info(f"Pasta de saída verificada/criada: {PASTA_SAIDA}")


def validar_pdf(pdf_path):
    # Verifica se o PDF é válido, retornando True se possui páginas.
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return len(pdf.pages) > 0
    except Exception:
        logging.warning(f"PDF inválido ou corrompido: {pdf_path}")
        return False


def processar_pdf(pdf_path, writer):
    # Abre o PDF e extrai tabelas de cada página, escrevendo os dados extraídos no CSV.
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
                            # Garante que cada linha tenha pelo menos 10 colunas, preenchendo com strings vazias.
                            while len(row) < 10:
                                row.append("")
                            writer.writerow(row)
    except Exception as e:
        logging.error(f"Erro ao processar PDF {pdf_path}: {e}")


def extrair_dados(pdf_path):
    # Executa o fluxo completo de extração de tabelas do PDF para um arquivo CSV.

    # Cria o diretório de saída, se necessário.
    criar_pasta_saida()
    csv_path = os.path.join(PASTA_SAIDA, "dados_extraidos.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Define e escreve o cabeçalho do CSV.
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

        # Verifica se o PDF é válido antes de prosseguir.
        if not validar_pdf(pdf_path):
            logging.error("O PDF fornecido é inválido ou corrompido.")
            return None

        # Processa o PDF e escreve as informações extraídas no CSV.
        processar_pdf(pdf_path, writer)

    logging.info(f"Extração concluída. Dados salvos em: {csv_path}")
    return csv_path


if __name__ == "__main__":
    # Define o caminho do PDF de exemplo e inicia o processo de extração.
    pdf_path = os.path.join(PASTA_ANEXOS, "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
    extrair_dados(pdf_path)
