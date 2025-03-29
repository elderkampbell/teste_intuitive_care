import os
import mysql.connector  # type: ignore
import requests  # type: ignore
import pandas as pd  # type: ignore

# Configurações do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "port": 33061,
    "user": "root",
    "password": "root",
    "database": "ans_dados",
}

# URL dos dados de operadoras
URL_OPERADORAS = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

# Diretório de download
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def conectar_bd():
    """Conecta ao banco de dados e retorna a conexão."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None


def criar_tabelas():
    """Cria as tabelas necessárias no banco de dados."""
    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()
    queries = [
        """
        CREATE TABLE IF NOT EXISTS operadoras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            registro_ans VARCHAR(10) NOT NULL,
            cnpj VARCHAR(18) NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(50),
            logradouro VARCHAR(255),
            numero VARCHAR(15),
            complemento VARCHAR(255),
            bairro VARCHAR(255),
            cidade VARCHAR(255),
            uf VARCHAR(2),
            cep VARCHAR(10),
            ddd VARCHAR(5),
            telefone VARCHAR(15),
            fax VARCHAR(50),
            endereco_eletronico VARCHAR(255),
            representante VARCHAR(255),
            cargo_representante VARCHAR(255),
            regiao_de_comercializacao VARCHAR(255),
            data_registro_ans DATE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data DATE,
                reg_ans VARCHAR(30),
                cd_conta_contabil VARCHAR(20),
                descricao VARCHAR(255),
                vl_saldo_inicial VARCHAR(30),
                vl_saldo_final VARCHAR(30)
        );
        """,
    ]

    for query in queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabelas criadas com sucesso!")


def importar_operadoras():
    """Baixa e importa os dados das operadoras ativas."""
    csv_path = os.path.join(DOWNLOAD_DIR, "Relatorio_cadop.csv")

    print("Baixando dados das operadoras...")
    response = requests.get(URL_OPERADORAS)
    if response.status_code == 200:
        with open(csv_path, "wb") as f:
            f.write(response.content)
        print("Arquivo de operadoras baixado!")
    else:
        print("Erro ao baixar os dados das operadoras.")
        return

    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    conn = conectar_bd()
    if not conn:
        return

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, uf, municipio, data_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row.get("Registro_ANS"),
                row.get("CNPJ"),
                row.get("Razao_Social"),
                row.get("Nome_Fantasia"),
                row.get("Modalidade"),
                row.get("UF"),
                row.get("Cidade"),
                row.get("Data_Registro_ANS"),
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Dados das operadoras importados com sucesso!")


def main():
    criar_tabelas()
    importar_operadoras()


if __name__ == "__main__":
    main()
