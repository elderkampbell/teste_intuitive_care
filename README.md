# Projeto de Extração e Processamento de Dados

Este projeto é uma aplicação para raspagem, extração e processamento de dados de arquivos PDF, além de realizar transformações e compactações nos arquivos gerados. O sistema integra uma API (desenvolvida com Flask) e um frontend (desenvolvido com Vue.js) para gerenciamento dos dados extraídos e processados no banco de dados.

## Funcionalidades

- **Raspagem e Download:**  
  - Raspagem de links de arquivos PDF em páginas web.  
  - Download em massa com execução paralela.
- **Processamento e Transformação:**  
  - Extração e transformação dos dados para o formato CSV.
  - Compactação dos arquivos gerados.
  - Geração de hashes para verificação de integridade.
- **API e Interface Web:**  
  - API RESTful em Flask para CRUD (busca, adição, edição e deleção) de operadoras.  
  - Frontend em Vue.js com layout responsivo, que permite a pesquisa, inclusão, edição e remoção de registros no banco.
- **Teste de API:**  
  - Implementação de uma rota para busca textual que retorna os registros mais relevantes conforme o CSV previamente inserido no banco.
  - Para validação dos endpoints da API, há uma coleção Postman incluída com o projeto.

## Pré-requisitos

- **Python 3 e pip**  
- **Node.js e npm**  
- **Banco de Dados MySQL**
> **Observação:** Recomenda-se o uso de um ambiente virtual para gerenciar as dependências.

## Clone o repositório

1. **Use o comando git clone seguido da ssh do repositório**

   ```bash
   git clone git@github.com:elderkampbell/teste_intuitive_care.git
   ```

2. **Acesse o Diretório do Repositório Clonado**

   Após o clone ser concluído, navegue até o diretório do repositório:

   ```bash
   cd teste_intuitive_care
   ```

## Configuração do Ambiente

1. **Crie o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   ```
   ou
   ```bash
   python -m venv .venv
   ```

2. **Ative o ambiente virtual:**
   - Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

> **Observação:** Para sair do ambiente virtual, utilize:
> ```bash
> source deactivate
> ```

## Configuração do Banco de Dados

Edite os arquivos `database_setup.py` e `app.py` para configurar o banco de dados, atualizando o objeto `DB_CONFIG` exemplificado abaixo:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 33061,
    "user": "root",
    "password": "root",
    "database": "ans_dados",
}
```

> **Atenção:** Certifique-se de que as configurações correspondem ao ambiente do seu banco.

## Estrutura do Projeto

```
projeto/
├── src/
│   ├── app.py                # Inicia o servidor Flask e o frontend Vue.js via a função preparar_vue().
│   ├── main.py               # Executa as funcionalidades principais do projeto: raspagem, download, processamento, transformação e compactação dos dados.
│   ├── parallel.py           # Download paralelo de arquivos.
│   ├── scraping.py           # Funções de raspagem de links e download de PDFs.
│   ├── transform.py          # Transformação e processamento dos dados CSV.
│   ├── utils.py              # Funções auxiliares para manipulação de arquivos, hashes e logs.
│   └── database_setup.py     # Configura as conexões e estrutura do banco de dados.
│   └── database_import.py    # Responsável por gerenciar o download, a extração e a importação dos dados para o banco de dados.
│
├── interface_vue_js/         # Diretório do frontend em Vue.js.
│   ├── package.json          # Dependências e scripts do Node.js.
│   ├── src/
│   │   └── App.vue           # Componente principal com funcionalidades de pesquisa, adição, edição e exclusão.
│   └── ...                   # Outros componentes e arquivos do Vue.js.
│
├── Coleção_Postman_Operadoras_API.json  # Arquivo para importação no Postman e execução dos testes da API.
├── requirements.txt          # Dependências Python.
├── tests/                    # Testes automatizados do projeto com pytest.
└── README.md                 # Este arquivo.
```

## Execução das Funcionalidades Principais

O arquivo `src/main.py` é responsável por executar o fluxo completo de processamento dos dados. Ao executar:

```bash
python3 -m src.main
```

O projeto realiza as seguintes etapas:

1. Raspagem dos links dos arquivos PDF do repositório público: [https://bit.ly/42fbBAw](https://bit.ly/42fbBAw).
2. Raspagem, download e extração dos dados dos últimos 2 anos do repositório público: [http://bit.ly/42p4s1I](http://bit.ly/42p4s1I).
3. Raspagem, download e importação do CSV do repositório: [https://bit.ly/3Rr44td](https://bit.ly/3Rr44td).
4. Download e armazenamento dos PDFs na pasta `\anexos`.
5. Extração, transformação e conversão dos dados para o formato CSV, armazenando na pasta `\saida`.
6. Compactação dos dados transformados em `Teste_elder_kampbell.zip`, armazenando na pasta `\anexos`.
7. Leitura e importação individual dos dados dos últimos 2 anos baixados para o banco de dados (DB).
8. Compactação dos arquivos gerados na pasta `\teste_intuitive_care`, nomeando o arquivo como `anexos_DDMMYYYY_HHMMSS`.
9. Consulta das 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE MÉDICO HOSPITALAR" no último trimestre.
10. Consulta das 10 operadoras com maiores despesas nessa categoria no último ano.
11. Exibição das respostas no terminal.

> **Obs.** Essa execução prepara os dados que serão posteriormente gerenciados via API e disponibilizados no frontend.

## Execução dos Servidores

O arquivo `src/app.py` integra o backend e o frontend. Ao executar:

```bash
python src/app.py
```

Será chamada a função `preparar_vue()`, que:
- Executa `npm install` na pasta `interface_vue_js` para instalar as dependências do Vue.js.
- Inicia o servidor de desenvolvimento do Vue.js com `npm run serve`.

A partir daí:
- O backend Flask roda em [http://127.0.0.1:5000](http://127.0.0.1:5000).
- O frontend Vue.js normalmente é servido em [http://localhost:8080](http://localhost:8080).

## Uso

### API (Flask)

A API está acessível através de `http://127.0.0.1:5000/buscar_operadoras?termo=`

A API permite as seguintes operações:

- **Busca de Operadoras:**  
  Endpoint: `GET /buscar_operadoras?termo=palavra-chave`  
  Retorna até 50 registros filtrados por *Nome Fantasia* ou *Razão Social*.

- **Adicionar Operadora:**  
  Endpoint: `POST /operadoras`  
  Recebe um JSON com os dados da operadora e insere o registro no banco.

- **Atualizar Operadora:**  
  Endpoint: `PUT /operadoras/<id>`  
  Atualiza apenas os campos modificados (atualização parcial).

- **Deletar Operadora:**  
  Endpoint: `DELETE /operadoras/<id>`  
  Remove o registro da operadora com o ID especificado.

### Frontend (Vue.js)

A interface web está acessível através de `http://localhost:8080/`

A interface permite:

- **Pesquisar Operadoras:**  
  Preencha o campo de busca e clique em "Buscar" para exibir uma lista filtrada por *Nome Fantasia* ou *Razão Social*.
- **Adicionar Operadora:**  
  Complete o formulário e clique em "Adicionar".
- **Editar Operadora:**  
  Selecione uma operadora, clique em "Editar" para preencher o formulário e, após as alterações, clique em "Atualizar". Apenas os campos alterados serão enviados.
- **Excluir Operadora:**  
  Clique em "Excluir" ao lado do registro desejado.

## Coleção Postman

> **Atenção:** Certifique-se de que a API esteja rodando em `127.0.0.1:5000` antes de iniciar os testes.

Na raiz do projeto, há o arquivo `Coleção_Postman_Operadoras_API.json`.

### Instruções de utilização:

1. **Importar a coleção:**  
   Abra o Postman e importe o arquivo `Coleção_Postman_Operadoras_API.json`.
2. **Executar os testes:**  
   Clique com o botão direito sobre a coleção importada e escolha a opção **Run Collection**.
3. **Visualizar os resultados:**  
   Os testes configurados para os endpoints da API serão executados automaticamente e você poderá visualizar os resultados na interface do Postman.

## Testes Automatizados

Para executar os testes, utilize os comandos:

```bash
pytest --cov=src
```
ou
```bash
pytest --cov
```

## Resumo dos Desafios ✅

<details>
  <summary>Clique para expandir</summary>

### 1. Teste de Web Scraping
- **Objetivo:** Realizar acesso a um site específico e baixar documentos relevantes.
- **Concluído:**
  - Acesso ao site designado.
  - Download dos Anexos I e II em formato PDF.
  - Compactação de todos os anexos em um único arquivo.

### 2. Teste de Transformação de Dados
- **Objetivo:** Extrair e estruturar dados de um dos PDFs baixados.
- **Concluído:**
  - Extração dos dados da tabela relevante do PDF.
  - Salvamento dos dados em formato CSV.
  - Compactação do arquivo CSV em um ZIP nomeado de forma apropriada.
  - Substituição de abreviações por descrições completas conforme necessário.

### 3. Teste de Banco de Dados
- **Objetivo:** Preparar e estruturar dados em um banco de dados.
- **Concluído:**
  - Download de arquivos necessários de repositórios públicos.
  - Criação de scripts SQL para estruturar tabelas.
  - Elaboração de queries para importar dados, garantindo o encoding correto.
  - Desenvolvimento de queries analíticas para responder a perguntas específicas sobre despesas de operadoras.

### 4. Teste de API
- **Objetivo:** Desenvolver uma interface web que interaja com um servidor.
- **Concluído:**
  - Utilização de um arquivo CSV previamente preparado no DB.
  - Implementação de rotas para busca textual, adição, exclusão e edição.
  - Criação de uma coleção Postman para demonstrar os endpoints e testar a API.
</details>