from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import logging
import subprocess
import threading

# Configuração de logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "port": 33061,
    "user": "root",
    "password": "root",
    "database": "ans_dados",
}


# Função para conexão com o banco de dados
def conectar_banco():
    try:
        conn = pymysql.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            cursorclass=pymysql.cursors.DictCursor,
        )
        logging.info("Conexão com o banco de dados estabelecida com sucesso!")
        return conn
    except Exception as e:
        logging.exception("Erro ao conectar com o banco de dados.")
        return None


@app.route("/buscar_operadoras", methods=["GET"])
def buscar_operadoras():
    termo = request.args.get("termo", "").lower()
    if not termo:
        return jsonify({"erro": "É necessário fornecer um termo de busca."}), 400

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            query = """
                SELECT Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, UF, Endereco_Eletronico
                FROM operadoras
                WHERE LOWER(Nome_Fantasia) LIKE %s OR LOWER(Razao_Social) LIKE %s
                LIMIT 50
            """
            termo_busca = f"%{termo}%"
            cursor.execute(query, (termo_busca, termo_busca))
            resultados = cursor.fetchall()
        return jsonify(resultados), 200
    except Exception as e:
        logging.exception("Erro ao executar consulta no banco de dados.")
        return jsonify({"erro": "Erro ao realizar busca no banco de dados."}), 500
    finally:
        conn.close()


def preparar_vue():
    """
    Função para rodar 'npm install' e iniciar o servidor Vue.js.
    """
    try:
        logging.info("Instalando dependências do Vue.js com npm install...")
        subprocess.run(["npm", "install"], cwd="./interface_vue_js", check=True)
        logging.info("Dependências instaladas com sucesso.")

        logging.info("Iniciando o servidor Vue.js...")
        subprocess.run(["npm", "run", "serve"], cwd="./interface_vue_js", check=True)
    except Exception as e:
        logging.exception("Erro ao preparar o servidor Vue.js.")


if __name__ == "__main__":
    # Iniciar o Vue.js em um thread separado
    vue_thread = threading.Thread(target=preparar_vue)
    vue_thread.start()

    # Iniciar o servidor Flask
    app.run(debug=True)
