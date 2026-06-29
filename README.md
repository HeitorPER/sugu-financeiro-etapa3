# SUGU — Financeiro e de Compras (Etapa 3)

Aplicação que acessa o banco de dados da **Etapa 2** (subsistema *Financeiro e de
Compras* do SUGU) e implementa funcionalidades sobre suas entidades e
relacionamentos, com **back-end em Python (FastAPI)** e **front-end em React (Vite)**.

## Arquitetura

```
React (Vite, porta 5173)  ──/api──►  FastAPI (Python, porta 8000)  ──psycopg2──►  PostgreSQL 14+ (sugu_financeiro)
```

A API reutiliza as *functions*, *triggers* e *procedures* criadas na Etapa 2
(ex.: `sp_registrar_compra`, `sp_homologar_licitacao`, `sp_registrar_pagamento`,
`sp_relatorio_orcamento`, `fn_saldo_orcamento`, `fn_saldo_nota`).

## Estrutura

```
db/        Scripts SQL da Etapa 2 (schema + índices, rotinas, carga de dados)
backend/   API FastAPI em Python (acesso ao banco)
frontend/  Aplicação React/Vite (telas das funcionalidades)
docs/      PDF de entrega, prints e scripts de geração
```

## Funcionalidades

1. Cadastro e atualização de **fornecedores** (FORNECEDOR)
2. **Efetuar compra** — COMPRA + FORNECEDOR + ORCAMENTO (procedure + triggers)
3. **Licitações e propostas** — PROPOSTA + LICITACAO + FORNECEDOR (homologação)
4. **Pagamentos** de notas fiscais — PAGAMENTO + NOTA_FISCAL
5. **Relatórios gerenciais** — saldo dos orçamentos e ranking de fornecedores

## Como executar

### 1. Banco de dados (PostgreSQL 14+ via Docker)

```bash
docker run -d --name sugu-postgres \
  -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16

# carregar os scripts (na ordem); o 01 recria a base sugu_financeiro:
docker exec -i sugu-postgres psql -U postgres < db/01_schema.sql
docker exec -i sugu-postgres psql -U postgres < db/02_routines.sql
docker exec -i sugu-postgres psql -U postgres < db/03_seed.sql
```

> Já existe um PostgreSQL local? Basta carregar os três scripts com o cliente
> `psql` (eles usam o meta-comando `\connect` para entrar na base recém-criada):
>
> ```bash
> psql -U postgres -f db/01_schema.sql
> psql -U postgres -f db/02_routines.sql
> psql -U postgres -f db/03_seed.sql
> ```
>
> As credenciais padrão são `postgres`/`postgres` em `localhost:5432` — ajuste em
> `backend/.env` se necessário (veja `backend/.env.example`).

### 2. Back-end (API Python)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
# docs interativas: http://127.0.0.1:8000/docs
```

### 3. Front-end (React)

```bash
cd frontend
npm install
npm run dev
# aplicação: http://localhost:5173
```

## Tecnologias

Python 3.13 · FastAPI · Uvicorn · psycopg2 · python-dotenv · React 18 · Vite ·
PostgreSQL 14+ · Docker.
