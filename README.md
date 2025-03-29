# Projeto de Extração e Processamento de Dados

Este projeto é uma aplicação robusta para raspagem, extração e processamento de dados de arquivos PDF, além de realizar transformações e compactações nos arquivos gerados. Ele foi projetado para ser modular, eficiente e de fácil manutenção.

## Funcionalidades

- Raspagem de links de arquivos PDF a partir de páginas web.
- Download em massa de arquivos PDF com suporte a execução paralela.
- Processamento e transformação de dados CSV.
- Compactação de arquivos para armazenamento eficiente.
- Geração de hashes para verificação de integridade dos dados.

## Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. Recomenda-se usar um ambiente virtual para melhor gestão das dependências.

## Configuração do Ambiente

1. **Criar o ambiente virtual**  
   ```bash
   python3 -m venv .venv
   ```
   ou
      ```bash
   python -m venv .venv
   ```

2. **Ativar o ambiente virtual**  
   - Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```

3. **Instalar dependências**  
   ```bash
   pip install -r requirements.txt
   ```

## Configuração do Banco de Dados

É necessário editar o arquivo `database_setup.py` para configurar o banco de dados. Atualize a variável `DB_CONFIG` conforme necessário:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 33061,
    "user": "root",
    "password": "root",
    "database": "ans_dados",
}
```

Certifique-se de que as informações correspondem ao ambiente de banco de dados que você está utilizando.

## Estrutura do Projeto

- `main.py`: Arquivo principal para iniciar a aplicação.
- `parallel.py`: Contém funcionalidades para download paralelo de arquivos.
- `scraping.py`: Inclui funções para raspagem de links e downloads.
- `transform.py`: Implementa transformações em dados CSV.
- `utils.py`: Funções auxiliares para manipulação de arquivos, hashes e logs.
- `database_setup.py`: Configurações para conexão com o banco de dados.
- `requirements.txt`: Lista de dependências do projeto.
- `tests/`: Testes automatizados para validação do código.

## Execução

Para rodar a aplicação, utilize o comando abaixo no terminal, após ativar o ambiente virtual:

```bash
python -m main
```

## Testes Automatizados

Execute os testes para verificar o funcionamento do projeto:

```bash
pytest --cov=src
```

Para rodar todos os testes:
```bash
pytest
```

## Ferramentas de Desenvolvimento

- **flake8**: Ferramenta de linting para conformidade de estilo de código.
  ```bash
  flake8 src/ tests/
  ```
- **black**: Formatação automática do código.
  ```bash
  black src/ tests/
  ```