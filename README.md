# MCP Server de usuários (com busca semântica)

Este projeto expõe 3 tools MCP para trabalhar com usuários:
- criar usuário
- buscar usuário por ID
- buscar usuários por similaridade semântica

A ideia é simples: os dados ficam no SQLite (`users.db`) e os vetores de embedding ficam no FAISS (`faiss_index/`).

## O que tem aqui

- `server.py`: sobe o servidor MCP e registra as tools
- `services/user_service.py`: regras de negócio
- `database/connect.py` e `database/database.py`: conexão SQLite e criação da tabela
- `embeddings.py`: geração de embedding com `sentence-transformers`
- `vector_store.py`: persistência e consulta no FAISS
- `models.py`: schemas Pydantic
- `tools_tests/`: testes das tools

---

## Pré-requisitos

Para rodar local:
- Python 3.11
- Pipenv

Para rodar em container:
- Docker

---

## Rodando com Docker (recomendado para quem quer testar rápido)

### 1) Build da imagem

```bash
docker build -t case-tecnico-mcp .
```

### 2) Subir o servidor

```bash
docker run -p 8000:8000 case-tecnico-mcp
```

Observação: a tabela `users` é criada automaticamente no startup do servidor.

### 4) Persistir dados entre execuções (opcional, mas recomendado)

Sem volume, o banco/índice podem se perder quando o container for removido. Para manter dados:

```bash
docker run -p 8000:8000 \
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

### 3) Subir o servidor

```bash
python server.py
```

Observação: a tabela `users` é criada automaticamente no startup do servidor.

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

## Como rodar os testes

Os testes estão na pasta `tools_tests/`.

### Rodar suite completa

Da raiz do projeto:

```bash
pipenv run python tools_tests/test_tools.py
```

Ou de dentro da pasta de testes:

```bash
cd tools_tests
python test_tools.py
```

### Rodar por etapa (separado)

```bash
cd tools_tests

python test_create_user.py
python test_get_user.py
python test_search_users.py
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

---

## Dicas para quem vai estudar/evoluir o projeto

- A tabela `users` é criada automaticamente no startup do servidor e também protegida no primeiro `create_user`.
- Se mudar o schema de usuário, revise:
  - `models.py`
  - `services/user_service.py`
  - testes em `tools_tests/`
- Se adicionar/remover uma tool:
  - atualizar `server.py`
  - atualizar `services/user_service.py`
  - criar/ajustar teste correspondente
  - registrar no `tools_tests/test_tools.py`

---

## Dependências principais

- `fastmcp`
- `sentence-transformers`
- `faiss-cpu`
- `email-validator`

Versão de Python do projeto: **3.11**.
