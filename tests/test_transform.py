import os
import csv
from src.transform import transformar_dados

PASTA_SAIDA = "saida"


def test_transformar_dados():
    """
    Testa se a função `transformar_dados` substitui corretamente as abreviações.
    """
    # Criamos a pasta de saída
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Criamos um CSV de teste com abreviações
    csv_path = os.path.join(PASTA_SAIDA, "teste.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
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
        writer.writerow(
            [
                "Consulta Odontológica",
                "1",
                "2023",
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

    try:
        # Executa a transformação
        csv_transformado = transformar_dados(csv_path)

        # Verifica se o arquivo CSV transformado foi criado
        assert os.path.exists(csv_transformado), "O CSV transformado não foi gerado."

        # Lê o CSV transformado
        with open(csv_transformado, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Verifica se as abreviações foram substituídas corretamente
        assert (
            rows[1][3] == "Seg. Odontológica"
        ), "A abreviação 'OD' não foi substituída corretamente."
        assert (
            rows[1][4] == "Seg. Ambulatorial"
        ), "A abreviação 'AMB' não foi substituída corretamente."

    finally:
        # Limpeza manual
        os.remove(csv_path)
        os.remove(csv_transformado)

        # Remove todos os arquivos restantes antes de excluir a pasta
        for arquivo in os.listdir(PASTA_SAIDA):
            os.remove(os.path.join(PASTA_SAIDA, arquivo))

        os.rmdir(PASTA_SAIDA)
