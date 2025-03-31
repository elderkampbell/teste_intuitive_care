import os
import logging
import csv

# Configura o logging com nível INFO e formato com data, nível e mensagem.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Diretório onde os arquivos transformados serão salvos.
PASTA_SAIDA = "saida"

# Mapeamento de abreviações para suas formas completas.
SUBSTITUICOES = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial",
}

def criar_pasta_saida():
    # Cria a pasta de saída se ela não existir.
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    logging.info(f"Pasta de saída verificada/criada: {PASTA_SAIDA}")

def transformar_dados(csv_path):
    # Define o caminho para o arquivo CSV transformado.
    csv_transformado = os.path.join(PASTA_SAIDA, "dados_transformados.csv")

    # Abre o CSV original para leitura e o transformado para escrita.
    with open(csv_path, "r", encoding="utf-8") as f_in, open(
        csv_transformado, "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        # Lê e escreve o cabeçalho apenas uma vez.
        primeiro_cabecalho = next(reader)
        writer.writerow(primeiro_cabecalho)

        # Processa cada linha, ignorando cabeçalhos duplicados.
        for row in reader:
            if row != primeiro_cabecalho:
                # Se houver pelo menos 7 colunas, realiza substituições nos índices 3 e 4.
                if len(row) > 6:
                    row[3] = SUBSTITUICOES.get(row[3], row[3])
                    row[4] = SUBSTITUICOES.get(row[4], row[4])
                writer.writerow(row)

    logging.info(f"Transformação concluída. Dados salvos em: {csv_transformado}")
    return csv_transformado

if __name__ == "__main__":
    # Define o caminho do CSV extraído para processamento.
    csv_extraido = os.path.join(PASTA_SAIDA, "dados_extraidos.csv")

    # Se o arquivo extraído existir, executa a transformação; caso contrário, registra um erro.
    if os.path.exists(csv_extraido):
        transformar_dados(csv_extraido)
    else:
        logging.error("Arquivo de extração não encontrado. Execute a extração primeiro.")
