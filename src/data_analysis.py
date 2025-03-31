import mysql.connector  # type: ignore
import logging

# Configuração do banco de dados para conexão com o MySQL.
db_config = {
    "host": "localhost",        # Endereço do servidor de banco
    "port": 33061,              # Porta configurada
    "user": "root",             # Usuário do banco
    "password": "root",         # Senha do banco
    "database": "ans_dados",    # Nome do banco de dados
}

def conectar_bd():
    # Tenta conectar ao banco de dados usando as configurações definidas.
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        logging.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Consulta SQL para obter o Top 10 de operadoras com maiores despesas no último trimestre.
query_trimestre = """
WITH despesas AS (
    SELECT 
        reg_ans,
        SUM(
            IFNULL(CAST(REPLACE(vl_saldo_final, ',', '.') AS DECIMAL(15,2)), 0) - 
            IFNULL(CAST(REPLACE(vl_saldo_inicial, ',', '.') AS DECIMAL(15,2)), 0)
        ) AS total_despesa,
        DATE_FORMAT(data, '%Y-%m') AS mes,
        GROUP_CONCAT(DISTINCT descricao ORDER BY descricao) AS descricao_agregada
    FROM demonstracoes_contabeis
    WHERE 
        (descricao LIKE '%EVENTOS%' OR descricao LIKE '%SINISTROS%' OR descricao LIKE '%ASSISTÊNCIA%' 
         OR descricao LIKE '%MÉDICO%' OR descricao LIKE '%HOSPITALAR%')
    GROUP BY reg_ans, mes
),
ultima_data AS (
    SELECT MAX(data) AS max_data FROM demonstracoes_contabeis
),
periodos AS (
    SELECT 
        DATE_FORMAT(max_data, '%Y-%m') AS ultimo_mes,
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 3 MONTH), '%Y-%m') AS trimestre_passado,
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 1 YEAR), '%Y-%m') AS ano_passado
    FROM ultima_data
)
SELECT d.reg_ans, 
       SUM(d.total_despesa) AS total_despesa,
       p.trimestre_passado AS periodo_inicio,
       p.ultimo_mes AS periodo_fim,
       GROUP_CONCAT(DISTINCT d.descricao_agregada ORDER BY d.descricao_agregada) AS descricao_agregada
FROM despesas d
JOIN periodos p ON d.mes BETWEEN p.trimestre_passado AND p.ultimo_mes
GROUP BY d.reg_ans, p.trimestre_passado, p.ultimo_mes
ORDER BY total_despesa DESC
LIMIT 10;
"""

# Consulta SQL para obter o Top 10 de operadoras com maiores despesas no último ano.
query_ano = """
WITH despesas AS (
    SELECT 
        reg_ans,
        SUM(
            IFNULL(CAST(REPLACE(vl_saldo_final, ',', '.') AS DECIMAL(15,2)), 0) - 
            IFNULL(CAST(REPLACE(vl_saldo_inicial, ',', '.') AS DECIMAL(15,2)), 0)
        ) AS total_despesa,
        DATE_FORMAT(data, '%Y-%m') AS mes,
        GROUP_CONCAT(DISTINCT descricao ORDER BY descricao) AS descricao_agregada
    FROM demonstracoes_contabeis
    WHERE 
        (descricao LIKE '%EVENTOS%' OR descricao LIKE '%SINISTROS%' OR descricao LIKE '%ASSISTÊNCIA%' 
         OR descricao LIKE '%MÉDICO%' OR descricao LIKE '%HOSPITALAR%')
    GROUP BY reg_ans, mes
),
ultima_data AS (
    SELECT MAX(data) AS max_data FROM demonstracoes_contabeis
),
periodos AS (
    SELECT 
        DATE_FORMAT(max_data, '%Y-%m') AS ultimo_mes,
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 3 MONTH), '%Y-%m') AS trimestre_passado,
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 1 YEAR), '%Y-%m') AS ano_passado
    FROM ultima_data
)
SELECT d.reg_ans, 
       SUM(d.total_despesa) AS total_despesa,
       p.ano_passado AS periodo_inicio,
       p.ultimo_mes AS periodo_fim,
       GROUP_CONCAT(DISTINCT d.descricao_agregada ORDER BY d.descricao_agregada) AS descricao_agregada
FROM despesas d
JOIN periodos p ON d.mes BETWEEN p.ano_passado AND p.ultimo_mes
GROUP BY d.reg_ans, p.ano_passado, p.ultimo_mes
ORDER BY total_despesa DESC
LIMIT 10;
"""

def executar_query(query, titulo):
    # Conecta ao banco de dados e, se a conexão for bem-sucedida, executa a consulta SQL.
    conexao = conectar_bd()
    if not conexao:
        return

    cursor = conexao.cursor()
    cursor.execute(query)  # Executa o comando SQL
    resultados = cursor.fetchall()  # Recupera todos os resultados

    print(f"\n{titulo}")
    print("=" * 50)

    # Determina a operadora com a maior despesa dentre os resultados.
    maior_despesa = None
    for (reg_ans, total_despesas, periodo_inicio, periodo_fim, descricao_agregada) in resultados:
        if maior_despesa is None or total_despesas > maior_despesa[1]:
            maior_despesa = (reg_ans, total_despesas, periodo_inicio, periodo_fim, descricao_agregada)

    # Exibe a operadora com a maior despesa.
    print(
        f"Operadora com a maior despesa: {maior_despesa[0]} - R$ {maior_despesa[1]:,.2f} (Período: {maior_despesa[2]} a {maior_despesa[3]})"
    )
    print("Descrição dos eventos:", maior_despesa[4])
    print("=" * 50)

    # Exibe o Top 10 de operadoras com maiores despesas.
    for (reg_ans, total_despesas, periodo_inicio, periodo_fim, descricao_agregada) in resultados:
        print(
            f"Operadora {reg_ans}: R$ {total_despesas:,.2f} (Período: {periodo_inicio} a {periodo_fim})"
        )
    print("=" * 50)

    # Fecha o cursor e encerra a conexão com o banco.
    cursor.close()
    conexao.close()

def main():
    # Executa as consultas e exibe os resultados para o último trimestre e para o último ano.
    executar_query(query_trimestre, "Top 10 Operadoras com Maiores Despesas no Último Trimestre")
    executar_query(query_ano, "Top 10 Operadoras com Maiores Despesas no Último Ano")

if __name__ == "__main__":
    main()
