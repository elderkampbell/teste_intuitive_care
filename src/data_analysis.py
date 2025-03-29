import mysql.connector  # type: ignore
import logging

# Configuração do banco de dados
db_config = {
    "host": "localhost",  # Endereço do servidor de banco de dados
    "port": 33061,  # Porta definida no database_setup.py
    "user": "root",  # Usuário para conexão com o banco
    "password": "root",  # Senha do banco de dados
    "database": "ans_dados",  # Nome do banco de dados
}


# Função para conectar ao banco de dados MySQL
def conectar_bd():
    try:
        # Retorna a conexão com o banco de dados usando a configuração acima
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        # Caso ocorra um erro na conexão, loga o erro
        logging.error(f"Erro ao conectar ao banco de dados: {err}")
        return None


# Consulta SQL 1: Top 10 operadoras com maiores despesas no último trimestre
query_trimestre = """
WITH despesas AS (
    SELECT 
        reg_ans,
        SUM(
            IFNULL(CAST(REPLACE(vl_saldo_final, ',', '.') AS DECIMAL(15,2)), 0) -  # Cálculo da despesa final
            IFNULL(CAST(REPLACE(vl_saldo_inicial, ',', '.') AS DECIMAL(15,2)), 0)   # Subtração da despesa inicial
        ) AS total_despesa,
        DATE_FORMAT(data, '%Y-%m') AS mes,  # Formatação do mês no formato YYYY-MM
        GROUP_CONCAT(DISTINCT descricao ORDER BY descricao) AS descricao_agregada  -- Agrupamento das descrições de despesas
    FROM demonstracoes_contabeis
    WHERE 
        (descricao LIKE '%EVENTOS%' OR descricao LIKE '%SINISTROS%' OR descricao LIKE '%ASSISTÊNCIA%' 
        OR descricao LIKE '%MÉDICO%' OR descricao LIKE '%HOSPITALAR%')  # Filtragem das descrições relacionadas a despesas
    GROUP BY reg_ans, mes  # Agrupamento por operadora e mês
),
ultima_data AS (
    SELECT MAX(data) AS max_data FROM demonstracoes_contabeis  # Data mais recente da tabela
),
periodos AS (
    SELECT 
        DATE_FORMAT(max_data, '%Y-%m') AS ultimo_mes,  # Último mês disponível
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 3 MONTH), '%Y-%m') AS trimestre_passado,  # Trimestre anterior
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 1 YEAR), '%Y-%m') AS ano_passado  # Ano passado
    FROM ultima_data
)
SELECT d.reg_ans, 
       SUM(d.total_despesa) AS total_despesa,  # Soma das despesas totais
       p.trimestre_passado AS periodo_inicio,  # Início do período
       p.ultimo_mes AS periodo_fim,  # Fim do período
       GROUP_CONCAT(DISTINCT d.descricao_agregada ORDER BY d.descricao_agregada) AS descricao_agregada  -- Descrição agregada
FROM despesas d
JOIN periodos p ON d.mes BETWEEN p.trimestre_passado AND p.ultimo_mes  # Relacionando os dados com o período
GROUP BY d.reg_ans, p.trimestre_passado, p.ultimo_mes  # Agrupando por operadora e período
ORDER BY total_despesa DESC  # Ordenando pela maior despesa
LIMIT 10;  # Limitando o resultado aos top 10
"""

# Consulta SQL 2: Top 10 operadoras com maiores despesas no último ano
query_ano = """
WITH despesas AS (
    SELECT 
        reg_ans,
        SUM(
            IFNULL(CAST(REPLACE(vl_saldo_final, ',', '.') AS DECIMAL(15,2)), 0) -  # Cálculo da despesa final
            IFNULL(CAST(REPLACE(vl_saldo_inicial, ',', '.') AS DECIMAL(15,2)), 0)   # Subtração da despesa inicial
        ) AS total_despesa,
        DATE_FORMAT(data, '%Y-%m') AS mes,  # Formatação do mês no formato YYYY-MM
        GROUP_CONCAT(DISTINCT descricao ORDER BY descricao) AS descricao_agregada  -- Agrupamento das descrições de despesas
    FROM demonstracoes_contabeis
    WHERE 
        (descricao LIKE '%EVENTOS%' OR descricao LIKE '%SINISTROS%' OR descricao LIKE '%ASSISTÊNCIA%' 
        OR descricao LIKE '%MÉDICO%' OR descricao LIKE '%HOSPITALAR%')  # Filtragem das descrições relacionadas a despesas
    GROUP BY reg_ans, mes  # Agrupamento por operadora e mês
),
ultima_data AS (
    SELECT MAX(data) AS max_data FROM demonstracoes_contabeis  # Data mais recente da tabela
),
periodos AS (
    SELECT 
        DATE_FORMAT(max_data, '%Y-%m') AS ultimo_mes,  # Último mês disponível
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 3 MONTH), '%Y-%m') AS trimestre_passado,  # Trimestre anterior
        DATE_FORMAT(DATE_SUB(max_data, INTERVAL 1 YEAR), '%Y-%m') AS ano_passado  # Ano passado
    FROM ultima_data
)
SELECT d.reg_ans, 
       SUM(d.total_despesa) AS total_despesa,  # Soma das despesas totais
       p.ano_passado AS periodo_inicio,  # Início do período
       p.ultimo_mes AS periodo_fim,  # Fim do período
       GROUP_CONCAT(DISTINCT d.descricao_agregada ORDER BY d.descricao_agregada) AS descricao_agregada  -- Descrição agregada
FROM despesas d
JOIN periodos p ON d.mes BETWEEN p.ano_passado AND p.ultimo_mes  # Relacionando os dados com o período
GROUP BY d.reg_ans, p.ano_passado, p.ultimo_mes  # Agrupando por operadora e período
ORDER BY total_despesa DESC  # Ordenando pela maior despesa
LIMIT 10;  # Limitando o resultado aos top 10
"""


# Função para executar a query e exibir os resultados
def executar_query(query, titulo):
    # Conecta ao banco de dados
    conexao = conectar_bd()
    if not conexao:
        return

    cursor = conexao.cursor()
    cursor.execute(query)  # Executa a consulta SQL
    resultados = cursor.fetchall()  # Obtém os resultados da consulta

    print(f"\n{titulo}")
    print("=" * 50)

    # Encontrar a operadora com a maior despesa
    maior_despesa = None
    for (
        reg_ans,
        total_despesas,
        periodo_inicio,
        periodo_fim,
        descricao_agregada,
    ) in resultados:
        if maior_despesa is None or total_despesas > maior_despesa[1]:
            maior_despesa = (
                reg_ans,
                total_despesas,
                periodo_inicio,
                periodo_fim,
                descricao_agregada,
            )

    # Exibir a operadora com maior despesa
    print(
        f"Operadora com a maior despesa: {maior_despesa[0]} - R$ {maior_despesa[1]:,.2f} (Período: {maior_despesa[2]} a {maior_despesa[3]})"
    )
    print("Descrição dos eventos:", maior_despesa[4])

    print("=" * 50)

    # Exibir o top 10 de operadoras com maiores despesas
    for (
        reg_ans,
        total_despesas,
        periodo_inicio,
        periodo_fim,
        descricao_agregada,
    ) in resultados:
        print(
            f"Operadora {reg_ans}: R$ {total_despesas:,.2f} (Período: {periodo_inicio} a {periodo_fim})"
        )

    print("=" * 50)

    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()


# Função principal para executar as consultas
def main():
    # Executa as queries para o último trimestre e ano
    executar_query(
        query_trimestre, "Top 10 Operadoras com Maiores Despesas no Último Trimestre"
    )
    executar_query(query_ano, "Top 10 Operadoras com Maiores Despesas no Último Ano")


# Execução do script
if __name__ == "__main__":
    main()
