import os
import logging
import csv

# Configuração de logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Diretório de saída para os arquivos transformados
PASTA_SAIDA = "saida"

# Dicionário para substituição das abreviações
SUBSTITUICOES = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial",
}


def criar_pasta_saida():
    """Cria a pasta de saída para os arquivos processados."""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    logging.info(f"Pasta de saída verificada/criada: {PASTA_SAIDA}")


def transformar_dados(csv_path):
    """Substitui abreviações no CSV e gera um novo arquivo transformado sem repetição de cabeçalhos.

    Parâmetros:
    csv_path (str): Caminho do arquivo CSV a ser transformado.

    Retorna:
    str: Caminho do arquivo CSV transformado.
    """
    # Define o caminho do arquivo CSV transformado
    csv_transformado = os.path.join(PASTA_SAIDA, "dados_transformados.csv")

    # Abre o arquivo CSV de entrada para leitura e o arquivo de saída para escrita
    with open(csv_path, "r", encoding="utf-8") as f_in, open(
        csv_transformado, "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        # Lê o primeiro cabeçalho e escreve no arquivo de saída
        primeiro_cabecalho = next(reader)
        writer.writerow(primeiro_cabecalho)  # Escreve o cabeçalho apenas uma vez

        # Processa cada linha do CSV
        for row in reader:
            if row != primeiro_cabecalho:  # Ignora repetições de cabeçalho
                # Verifica se há pelo menos 7 colunas
                if len(row) > 6:
                    # Substitui abreviações nas colunas corretas (índices 3 e 4)
                    row[3] = SUBSTITUICOES.get(
                        row[3], row[3]
                    )  # Substitui 'Seg. Odontológica'
                    row[4] = SUBSTITUICOES.get(
                        row[4], row[4]
                    )  # Substitui 'Seg. Ambulatorial'
                writer.writerow(row)  # Escreve a linha transformada no arquivo de saída

    logging.info(f"Transformação concluída. Dados salvos em: {csv_transformado}")
    return csv_transformado


if __name__ == "__main__":
    # Define o caminho do arquivo CSV extraído
    csv_extraido = os.path.join(PASTA_SAIDA, "dados_extraidos.csv")

    # Verifica se o arquivo de extração existe antes de tentar transformá-lo
    if os.path.exists(csv_extraido):
        transformar_dados(csv_extraido)  # Chama a função para transformar os dados
    else:
        logging.error(
            "Arquivo de extração não encontrado. Execute a extração primeiro."
        )
