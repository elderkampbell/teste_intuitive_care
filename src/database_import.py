import os
import zipfile
import requests  # type: ignore
import pandas as pd  # type: ignore
import logging
from .database_setup import conectar_bd

# Diretórios para armazenamento
DIRETORIO_ANEXOS = "downloads"
DIRETORIO_EXTRAIDOS = "relatorios"
os.makedirs(DIRETORIO_ANEXOS, exist_ok=True)
os.makedirs(DIRETORIO_EXTRAIDOS, exist_ok=True)

# Configuração dos anos e trimestres
ANOS = ["2023", "2024"]
TRIMESTRES = ["1T", "2T", "3T", "4T"]
URL_BASE = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
URL_OPERADORAS = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"


def baixar_arquivos():
    """Baixa os arquivos ZIP das demonstrações contábeis."""
    for ano in ANOS:
        for trimestre in TRIMESTRES:
            zip_url = f"{URL_BASE}{ano}/{trimestre}{ano}.zip"
            zip_path = os.path.join(DIRETORIO_ANEXOS, f"{trimestre}{ano}.zip")

            if os.path.exists(zip_path):
                logging.info(f"Arquivo {zip_path} já existe. Pulando download.")
                continue

            logging.info(f"Baixando {zip_url}...")
            response = requests.get(zip_url)
            if response.status_code == 200:
                with open(zip_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"Arquivo {zip_path} baixado com sucesso!")
            else:
                logging.error(f"Erro ao baixar {zip_url}")


def extrair_zip():
    """Extrai todos os arquivos ZIP baixados."""
    for arquivo in os.listdir(DIRETORIO_ANEXOS):
        if arquivo.endswith(".zip"):
            zip_path = os.path.join(DIRETORIO_ANEXOS, arquivo)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(DIRETORIO_EXTRAIDOS)
            logging.info(f"Extraído: {zip_path}")


def corrigir_dados(df):
    """Corrige os formatos de data e valores numéricos."""
    if "DATA" in df.columns:
        try:
            df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True).dt.strftime(
                "%Y-%m-%d"
            )
        except Exception as e:
            logging.error(f"Erro ao converter datas: {e}")

    for coluna in ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.replace(",", ".").astype(float)

    return df


def importar_demonstracoes():
    """Importa os dados das demonstrações contábeis para o banco de dados."""
    arquivos_csv = [f for f in os.listdir(DIRETORIO_EXTRAIDOS) if f.endswith(".csv")]
    conexao = conectar_bd()
    if not conexao:
        return

    cursor = conexao.cursor()

    for arquivo in arquivos_csv:
        caminho_csv = os.path.join(DIRETORIO_EXTRAIDOS, arquivo)
        logging.info(f"Processando arquivo {arquivo}...")

        try:
            df = pd.read_csv(caminho_csv, delimiter=";", encoding="utf-8", dtype=str)
            df = corrigir_dados(df)
            logging.info(f"Arquivo {arquivo} carregado com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao carregar arquivo {arquivo}: {e}")
            continue

        colunas_esperadas = {
            "DATA",
            "REG_ANS",
            "CD_CONTA_CONTABIL",
            "DESCRICAO",
            "VL_SALDO_INICIAL",
            "VL_SALDO_FINAL",
        }
        if not colunas_esperadas.issubset(df.columns):
            logging.error(
                f"Colunas inesperadas no arquivo {arquivo}. Pulando importação."
            )
            continue

        for _, row in df.iterrows():
            try:
                cursor.execute(
                    """
                    INSERT INTO demonstracoes_contabeis (
                                                            data, 
                                                            reg_ans, 
                                                            cd_conta_contabil, 
                                                            descricao, 
                                                            vl_saldo_inicial, 
                                                            vl_saldo_final
                                                        )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        row.get("DATA"),
                        row.get("REG_ANS"),
                        row.get("CD_CONTA_CONTABIL"),
                        row.get("DESCRICAO"),
                        row.get("VL_SALDO_INICIAL"),
                        row.get("VL_SALDO_FINAL"),
                    ),
                )
            except Exception as e:
                logging.error(f"Erro ao processar linha do arquivo {arquivo}: {e}")

        conexao.commit()
        logging.info(f"Arquivo {arquivo} importado com sucesso!")

    cursor.close()
    conexao.close()


def importar_operadoras():
    """Baixa e importa os dados das operadoras ativas."""
    csv_path = os.path.join(DIRETORIO_ANEXOS, "Relatorio_cadop.csv")

    logging.info("Baixando dados das operadoras...")
    response = requests.get(URL_OPERADORAS)
    if response.status_code == 200:
        with open(csv_path, "wb") as f:
            f.write(response.content)
        logging.info("Arquivo de operadoras baixado!")
    else:
        logging.error("Erro ao baixar os dados das operadoras.")
        return

    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    conexao = conectar_bd()
    if not conexao:
        return

    cursor = conexao.cursor()

    for _, row in df.iterrows():

        try:
            cursor.execute(
                """
                INSERT INTO operadoras (
                                            registro_ans,
                                            cnpj, 
                                            razao_social, 
                                            nome_fantasia, 
                                            modalidade, 
                                            logradouro, 
                                            numero, 
                                            complemento, 
                                            bairro, 
                                            cidade, 
                                            uf, 
                                            cep, 
                                            ddd, 
                                            telefone, 
                                            fax, 
                                            endereco_eletronico, 
                                            representante, 
                                            cargo_representante, 
                                            regiao_de_comercializacao, 
                                            data_registro_ans
                                        )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                tuple(
                    None if pd.isna(row[col]) else row[col]
                    for col in [
                        "Registro_ANS",
                        "CNPJ",
                        "Razao_Social",
                        "Nome_Fantasia",
                        "Modalidade",
                        "Logradouro",
                        "Numero",
                        "Complemento",
                        "Bairro",
                        "Cidade",
                        "UF",
                        "CEP",
                        "DDD",
                        "Telefone",
                        "Fax",
                        "Endereco_eletronico",
                        "Representante",
                        "Cargo_Representante",
                        "Regiao_de_Comercializacao",
                        "Data_Registro_ANS",
                    ]
                ),
            )
        except Exception as e:
            logging.error(f"Erro ao processar linha: {e}")
    conexao.commit()
    cursor.close()
    conexao.close()
    logging.info("Dados das operadoras importados com sucesso!")


def importar_dados():
    """Executa a importação completa dos dados."""
    baixar_arquivos()
    extrair_zip()
    importar_demonstracoes()
    importar_operadoras()


if __name__ == "__main__":
    importar_dados()
