import os
import csv
from src.transform import transformar_dados

PASTA_SAIDA = "saida"


def test_transformar_dados():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
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
        csv_transformado = transformar_dados(csv_path)
        assert os.path.exists(csv_transformado), "O CSV transformado não foi gerado."
        with open(csv_transformado, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert (
            rows[1][3] == "Seg. Odontológica"
        ), "A abreviação 'OD' não foi substituída corretamente."
        assert (
            rows[1][4] == "Seg. Ambulatorial"
        ), "A abreviação 'AMB' não foi substituída corretamente."
    finally:
        os.remove(csv_path)
        os.remove(csv_transformado)
        for arquivo in os.listdir(PASTA_SAIDA):
            os.remove(os.path.join(PASTA_SAIDA, arquivo))
        os.rmdir(PASTA_SAIDA)
