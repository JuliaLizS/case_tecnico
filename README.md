# MCP Server de usuários (com busca semântica)

Este projeto expõe 4 tools MCP para trabalhar com usuários:
- criar usuário
- buscar usuário por ID
- buscar usuários por similaridade semântica
- listar usuários com paginação

A ideia é simples: os dados ficam no SQLite (`users.db`) e os vetores de embedding ficam no FAISS (`faiss_index/`).

## Quickstart (3 comandos)

```bash
pipenv install
pipenv run streamlit run app.py
pipenv run pytest tools_tests -q
```

> Dica: rode o `pytest` em outro terminal se o servidor estiver em execução no primeiro.

## O que tem aqui

- `server.py`: sobe o servidor MCP e registra as tools
- `app.py`: interface Streamlit para testar as funcionalidades
- `services/user_service.py`: regras de negócio
- `database/connect.py` e `database/database.py`: conexão SQLite e criação da tabela
- `embeddings.py`: geração de embedding com `sentence-transformers`
- `vector_store.py`: persistência e consulta no FAISS
- `models.py`: schemas Pydantic
- `logging_config.py`: logging estruturado em JSON
- `tools_tests/`: testes das tools

---

## Pré-requisitos

Para rodar local:
- Python 3.11
- Pipenv

Para rodar em container:
- Docker

---

## Rodando com Docker

### 1) Build da imagem

```bash
docker build -t case-tecnico-mcp .
```

### 2) Subir no modo MCP (server)

```bash
docker run -p 8000:8000 \
  -e APP_MODE=mcp \
  -v $(pwd)/users.db:/app/users.db \
  -v $(pwd)/faiss_index:/app/faiss_index \
  case-tecnico-mcp
```

### 3) Subir no modo Streamlit (front para testes)

```bash
docker run -p 8501:8501 \
  -e APP_MODE=streamlit \
  -v $(pwd)/users.db:/app/users.db \
  -v $(pwd)/faiss_index:/app/faiss_index \
  case-tecnico-mcp
```

Abra no navegador:
- `http://localhost:8501` (Streamlit)

Observações:
- A tabela `users` é criada automaticamente no startup.
- No primeiro boot, o modelo de embedding pode demorar para baixar do Hugging Face.
- Docker Compose não é obrigatório neste projeto (apenas um serviço).

### 4) Persistir dados entre execuções (recomendado)

Sem volume, o banco/índice podem se perder quando o container for removido. Para manter dados:

```bash
docker run -p 8000:8000 \
  -e APP_MODE=mcp \
  -v $(pwd)/users.db:/app/users.db \
  -v $(pwd)/faiss_index:/app/faiss_index \
  case-tecnico-mcp
```

---

## Rodando local com Pipenv

### 1) Instalar dependências

```bash
pipenv install
```

### 2) Entrar no ambiente virtual

```bash
pipenv shell
```

### 3) Rodar em modo MCP (server)

```bash
python server.py
```

### 4) Rodar em modo Streamlit (front para testes)

```bash
streamlit run app.py
```

Observação: a tabela `users` é criada automaticamente no startup do serviço.

---

## Tools disponíveis

## 1) `create_user`

Cria usuário no SQLite e salva embedding no FAISS.

### Entrada

```json
{
  "name": "Ana Silva",
  "email": "ana.silva@example.com",
  "description": "Engenheira backend Python com foco em APIs"
}
```

### Saída (sucesso)

```json
{
  "message": "Usuário criado com sucesso",
  "user_id": 1
}
```

### Saída (erro comum)

```json
{
  "error": "UNIQUE constraint failed: users.email"
}
```

---

## 2) `get_user`

Busca um usuário por ID.

### Entrada

```json
{
  "user_id": 1
}
```

### Saída (sucesso)

```json
{
  "id": 1,
  "name": "Ana Silva",
  "email": "ana.silva@example.com",
  "description": "Engenheira backend Python com foco em APIs"
}
```

### Saída (não encontrado)

```json
{
  "error": "Usuario com ID 999 não encontrado"
}
```

---

## 3) `search_users`

Faz busca semântica por texto usando embedding + FAISS.

### Entrada

```json
{
  "query": "backend python api",
  "top_k": 3
}
```

### Saída (exemplo)

```json
[
  {
    "id": 1,
    "name": "Ana Silva",
    "email": "ana.silva@example.com",
    "description": "Engenheira backend Python com foco em APIs",
    "score": 0.3867
  }
]
```

Observação: no score do FAISS (L2), quanto menor, mais próximo semanticamente.

---

## 4) `list_users`

Lista usuários com paginação por `limit` e `offset`.

### Entrada

```json
{
  "limit": 10,
  "offset": 0
}
```

### Saída (exemplo)

```json
[
  {
    "id": 1,
    "name": "Ana Silva",
    "email": "ana.silva@example.com",
    "description": "Engenheira backend Python com foco em APIs"
  },
  {
    "id": 2,
    "name": "Carlos Mendes",
    "email": "carlos.mendes@example.com",
    "description": "Cientista de dados com foco em machine learning e análise de dados"
  }
]
```

---

## Como rodar os testes

Os testes estão na pasta `tools_tests/`.

### Rodar suite completa

Da raiz do projeto:

```bash
pipenv run pytest tools_tests -q
```

Ou de dentro da pasta de testes:

```bash
cd tools_tests
pytest -q
```

### Rodar por etapa (separado)

```bash
pipenv run pytest tools_tests/test_create_user.py -q
pipenv run pytest tools_tests/test_get_user.py -q
pipenv run pytest tools_tests/test_search_users.py -q
pipenv run pytest tools_tests/test_list_users.py -q
```

### O que cada teste cobre

- `test_create_user.py`
  - criação de usuários válidos
  - tentativa de e-mail duplicado
  - validação de e-mail inválido

- `test_get_user.py`
  - busca por ID existente
  - busca por ID inexistente
  - busca por ID negativo

- `test_search_users.py`
  - consultas semânticas com validação de relevância
  - validação de `top_k`
  - query vazia sem quebrar execução

- `test_list_users.py`
  - listagem básica
  - validação de paginação (`limit`/`offset`)
  - offset fora do range retorna lista vazia

---

## Dicas para quem vai estudar/evoluir o projeto

- A tabela `users` é criada automaticamente na inicialização do serviço (fase de startup).
- Se mudar o schema de usuário, revise:
  - `models.py`
  - `services/user_service.py`
  - testes em `tools_tests/`
- Se adicionar/remover uma tool:
  - atualizar `server.py`
  - atualizar `services/user_service.py`
  - criar/ajustar teste correspondente
  - garantir cobertura em `tools_tests/` e validar com `pytest`
- O índice FAISS usa caminho absoluto baseado na raiz do projeto, então não depende do diretório de execução.

---

## Dependências principais

- `fastmcp`
- `sentence-transformers`
- `faiss-cpu`
- `email-validator`

Versão de Python do projeto: **3.11**.
