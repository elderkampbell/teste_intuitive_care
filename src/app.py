from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import logging
import subprocess
import threading

# Configura o logging para nível INFO
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# Configurações de conexão com o banco de dados
db_config = {
    "host": "localhost",
    "port": 33061,
    "user": "root",
    "password": "root",
    "database": "ans_dados",
}

def conectar_banco():
    # Tenta estabelecer a conexão com o banco de dados usando pymysql
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
    # Obtém o termo de busca a partir dos parâmetros da URL e converte para minúsculo
    termo = request.args.get("termo", "").lower()
    if not termo:
        return jsonify({"erro": "É necessário fornecer um termo de busca."}), 400

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            # Consulta as operadoras com base no termo de busca, comparando nome e razão social
            query = """
                SELECT 
                  id,
                  registro_ans AS Registro_ANS,
                  cnpj AS CNPJ,
                  razao_social AS Razao_Social,
                  nome_fantasia AS Nome_Fantasia,
                  modalidade AS Modalidade,
                  logradouro AS Logradouro,
                  numero AS Numero,
                  complemento AS Complemento,
                  bairro AS Bairro,
                  cidade AS Cidade,
                  uf AS UF,
                  cep AS CEP,
                  ddd AS DDD,
                  telefone AS Telefone,
                  fax AS Fax,
                  endereco_eletronico AS Endereco_eletronico,
                  representante AS Representante,
                  cargo_representante AS Cargo_Representante,
                  regiao_de_comercializacao AS Regiao_de_Comercializacao,
                  data_registro_ans AS Data_Registro_ANS
                FROM operadoras
                WHERE LOWER(nome_fantasia) LIKE %s OR LOWER(razao_social) LIKE %s
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

@app.route("/operadoras", methods=["POST"])
def adicionar_operadora():
    # Recebe os dados da nova operadora via JSON
    dados = request.json
    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            # Insere os dados na tabela 'operadoras'
            query = """
                INSERT INTO operadoras (
                    registro_ans, cnpj, razao_social, nome_fantasia, modalidade, 
                    logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, 
                    telefone, fax, endereco_eletronico, representante, cargo_representante, 
                    regiao_de_comercializacao, data_registro_ans
                )
                VALUES (
                    %(Registro_ANS)s, %(CNPJ)s, %(Razao_Social)s, %(Nome_Fantasia)s, %(Modalidade)s, 
                    %(Logradouro)s, %(Numero)s, %(Complemento)s, %(Bairro)s, %(Cidade)s, %(UF)s, %(CEP)s, %(DDD)s, 
                    %(Telefone)s, %(Fax)s, %(Endereco_eletronico)s, %(Representante)s, %(Cargo_Representante)s, 
                    %(Regiao_de_Comercializacao)s, %(Data_Registro_ANS)s
                )
            """
            cursor.execute(query, dados)
            conn.commit()
        return jsonify({"mensagem": "Operadora adicionada com sucesso!"}), 201
    except Exception as e:
        logging.exception("Erro ao adicionar operadora.")
        return jsonify({"erro": "Erro ao adicionar operadora."}), 500
    finally:
        conn.close()

@app.route("/operadoras/<int:id>", methods=["PUT"])
def atualizar_operadora(id):
    # Atualiza os dados da operadora identificada pelo id
    dados = request.json
    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido para atualização."}), 400

    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            # Cria a cláusula SET dinamicamente a partir dos dados fornecidos
            set_clause = ", ".join([f"{chave.lower()}=%({chave})s" for chave in dados.keys()])
            query = f"UPDATE operadoras SET {set_clause} WHERE id=%(id)s"
            dados["id"] = id
            cursor.execute(query, dados)
            conn.commit()
        return jsonify({"mensagem": "Operadora atualizada com sucesso!"}), 200
    except Exception as e:
        logging.exception("Erro ao atualizar operadora.")
        return jsonify({"erro": "Erro ao atualizar operadora."}), 500
    finally:
        conn.close()

@app.route("/operadoras/<int:id>", methods=["DELETE"])
def deletar_operadora(id):
    # Deleta a operadora identificada pelo id
    conn = conectar_banco()
    if conn is None:
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM operadoras WHERE id=%s"
            cursor.execute(query, (id,))
            conn.commit()
        return jsonify({"mensagem": "Operadora deletada com sucesso!"}), 200
    except Exception as e:
        logging.exception("Erro ao deletar operadora.")
        return jsonify({"erro": "Erro ao deletar operadora."}), 500
    finally:
        conn.close()

def preparar_vue():
    # Prepara o ambiente do Vue.js executando o 'npm install' e iniciando o servidor
    try:
        logging.info("Instalando dependências do Vue.js com npm install...")
        subprocess.run(["npm", "install"], cwd="./interface_vue_js", check=True)
        logging.info("Dependências instaladas com sucesso.")

        logging.info("Iniciando o servidor Vue.js...")
        subprocess.run(["npm", "run", "serve"], cwd="./interface_vue_js", check=True)
    except Exception as e:
        logging.exception("Erro ao preparar o servidor Vue.js.")

if __name__ == "__main__":
    # Inicia o servidor Vue.js em uma thread separada e, em seguida, inicia o Flask em modo debug.
    vue_thread = threading.Thread(target=preparar_vue)
    vue_thread.start()
    app.run(debug=True)
