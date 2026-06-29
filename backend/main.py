"""
API REST (FastAPI) do subsistema Financeiro e de Compras do SUGU.

Cada endpoint acessa o banco PostgreSQL da Etapa 2 e exercita as
restricoes, functions, triggers e procedures ja existentes. As
funcionalidades envolvem sempre 2+ entidades e 1+ relacionamento:

  1. Fornecedores ............ CRUD em FORNECEDOR
  2. Efetuar compra .......... COMPRA + FORNECEDOR + ORCAMENTO (sp_registrar_compra)
  3. Licitacoes/Propostas .... PROPOSTA + LICITACAO + FORNECEDOR (sp_homologar_licitacao)
  4. Notas/Pagamentos ........ PAGAMENTO + NOTA_FISCAL (sp_registrar_pagamento)
  5. Relatorios gerenciais ... ORCAMENTO + COMPRA + FORNECEDOR (sp_relatorio_orcamento)
"""
from datetime import date
from decimal import Decimal
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from db import db_cursor, get_connection

app = FastAPI(title="SUGU - Financeiro e Compras", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------
# Tratamento uniforme de erros vindos do banco (triggers, CHECK, UNIQUE, FK)
# --------------------------------------------------------------------------
def db_error_to_http(exc: Exception) -> HTTPException:
    """Converte erros do PostgreSQL em respostas HTTP 400 amigaveis."""
    if isinstance(exc, psycopg2.Error):
        # RAISE EXCEPTION das triggers/procedures (regra de negocio),
        # alem de violacoes de CHECK, UNIQUE e FK.
        diag = getattr(exc, "diag", None)
        msg = (diag.message_primary if diag and diag.message_primary
               else str(exc).strip())
        return HTTPException(status_code=400, detail=msg)
    return HTTPException(status_code=500, detail=str(exc))


# ============================ MODELOS (entrada) ============================
class FornecedorIn(BaseModel):
    nome: str = Field(..., max_length=100)
    cnpj: str = Field(..., max_length=18)
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    regularidade_fiscal: str = "PENDENTE"


class RegularidadeIn(BaseModel):
    regularidade_fiscal: str


class CompraIn(BaseModel):
    data: date
    valor_total: Decimal
    id_fornecedor: int
    id_orcamento: int
    id_licitacao: Optional[int] = None


class PropostaIn(BaseModel):
    valor: Decimal
    data: date
    id_fornecedor: int
    id_licitacao: int


class HomologarIn(BaseModel):
    id_proposta: int


class PagamentoIn(BaseModel):
    id_nota: int
    valor: Decimal
    forma_pagamento: str
    data: date


# ================================ DASHBOARD ===============================
@app.get("/api/dashboard")
def dashboard():
    with db_cursor() as cur:
        cur.execute("""
            SELECT
              (SELECT COUNT(*) FROM FORNECEDOR) AS fornecedores,
              (SELECT COUNT(*) FROM FORNECEDOR WHERE regularidade_fiscal='REGULAR') AS fornecedores_regulares,
              (SELECT COUNT(*) FROM COMPRA) AS compras,
              (SELECT COALESCE(SUM(valor_total),0) FROM COMPRA) AS total_comprado,
              (SELECT COUNT(*) FROM LICITACAO WHERE status IN ('ABERTA','EM_ANALISE')) AS licitacoes_abertas,
              (SELECT COALESCE(SUM(valor_total - valor_consumido),0) FROM ORCAMENTO) AS saldo_total
        """)
        return cur.fetchone()


# ============================ 1. FORNECEDORES =============================
@app.get("/api/fornecedores")
def listar_fornecedores():
    with db_cursor() as cur:
        cur.execute("""
            SELECT id_fornecedor, nome, cnpj, endereco, telefone, regularidade_fiscal
              FROM FORNECEDOR ORDER BY nome
        """)
        return cur.fetchall()


@app.post("/api/fornecedores", status_code=201)
def criar_fornecedor(f: FornecedorIn):
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO FORNECEDOR (nome, cnpj, endereco, telefone, regularidade_fiscal)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_fornecedor
            """, (f.nome, f.cnpj, f.endereco, f.telefone, f.regularidade_fiscal))
            new_id = cur.fetchone()["id_fornecedor"]
        return {"id_fornecedor": new_id, "mensagem": "Fornecedor cadastrado com sucesso."}
    except Exception as exc:
        raise db_error_to_http(exc)


@app.put("/api/fornecedores/{id_fornecedor}/regularidade")
def atualizar_regularidade(id_fornecedor: int, r: RegularidadeIn):
    try:
        with db_cursor(commit=True) as cur:
            cur.execute(
                "UPDATE FORNECEDOR SET regularidade_fiscal=%s WHERE id_fornecedor=%s",
                (r.regularidade_fiscal, id_fornecedor),
            )
            if cur.rowcount == 0:
                raise HTTPException(404, "Fornecedor nao encontrado.")
        return {"mensagem": "Regularidade fiscal atualizada."}
    except HTTPException:
        raise
    except Exception as exc:
        raise db_error_to_http(exc)


# =============================== 2. COMPRAS ==============================
@app.get("/api/orcamentos")
def listar_orcamentos():
    """Orcamentos com saldo calculado pela function fn_saldo_orcamento."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT id_orcamento, ano, setor, departamento, projeto,
                   valor_total, valor_consumido,
                   fn_saldo_orcamento(id_orcamento) AS saldo
              FROM ORCAMENTO ORDER BY ano, setor
        """)
        return cur.fetchall()


@app.get("/api/compras")
def listar_compras():
    """COMPRA juntando FORNECEDOR e ORCAMENTO (relacionamentos realiza/financia)."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT c.id_compra, c.data, c.valor_total,
                   f.nome AS fornecedor, o.setor AS orcamento_setor,
                   o.projeto AS orcamento_projeto, c.id_licitacao
              FROM COMPRA c
              JOIN FORNECEDOR f ON f.id_fornecedor = c.id_fornecedor
              JOIN ORCAMENTO  o ON o.id_orcamento  = c.id_orcamento
             ORDER BY c.id_compra DESC
        """)
        return cur.fetchall()


@app.post("/api/compras", status_code=201)
def efetuar_compra(c: CompraIn):
    """
    Efetua uma compra chamando a procedure sp_registrar_compra.
    As triggers trg_compra_before_insert (regularidade + saldo) e
    trg_compra_after_insert (atualiza valor_consumido) atuam aqui.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # No PostgreSQL o parametro INOUT e passado como NULL e o valor
            # de saida e devolvido pelo proprio CALL como um conjunto de
            # resultados de uma unica linha/coluna.
            cur.execute(
                "CALL sp_registrar_compra(%s, %s, %s, %s, %s, NULL)",
                (c.data, c.valor_total, c.id_fornecedor, c.id_licitacao, c.id_orcamento),
            )
            new_id = next(iter(cur.fetchone().values()))
        conn.commit()
        return {"id_compra": new_id, "mensagem": f"Compra #{new_id} registrada com sucesso."}
    except Exception as exc:
        conn.rollback()
        raise db_error_to_http(exc)
    finally:
        conn.close()


# ====================== 3. LICITACOES E PROPOSTAS =======================
@app.get("/api/licitacoes")
def listar_licitacoes():
    """LICITACAO com numero de propostas pela function fn_qtd_propostas."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT id_licitacao, tipo, data_inicio, data_fim, status,
                   fn_qtd_propostas(id_licitacao) AS qtd_propostas
              FROM LICITACAO ORDER BY id_licitacao
        """)
        return cur.fetchall()


@app.get("/api/licitacoes/{id_licitacao}/propostas")
def propostas_da_licitacao(id_licitacao: int):
    """PROPOSTA + FORNECEDOR de uma licitacao (relacionamento envia)."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT p.id_proposta, p.valor, p.data, p.vencedora,
                   f.id_fornecedor, f.nome AS fornecedor, f.regularidade_fiscal
              FROM PROPOSTA p
              JOIN FORNECEDOR f ON f.id_fornecedor = p.id_fornecedor
             WHERE p.id_licitacao = %s
             ORDER BY p.valor
        """, (id_licitacao,))
        return cur.fetchall()


@app.post("/api/propostas", status_code=201)
def criar_proposta(p: PropostaIn):
    """Insere PROPOSTA; trigger trg_proposta_before_insert exige licitacao aberta."""
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO PROPOSTA (valor, data, id_fornecedor, id_licitacao)
                VALUES (%s, %s, %s, %s)
                RETURNING id_proposta
            """, (p.valor, p.data, p.id_fornecedor, p.id_licitacao))
            new_id = cur.fetchone()["id_proposta"]
        return {"id_proposta": new_id, "mensagem": "Proposta registrada com sucesso."}
    except Exception as exc:
        raise db_error_to_http(exc)


@app.post("/api/licitacoes/{id_licitacao}/homologar")
def homologar_licitacao(id_licitacao: int, h: HomologarIn):
    """Chama a procedure sp_homologar_licitacao (marca vencedora + status)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL sp_homologar_licitacao(%s, %s)", (id_licitacao, h.id_proposta))
        conn.commit()
        return {"mensagem": f"Licitacao {id_licitacao} homologada (proposta {h.id_proposta} vencedora)."}
    except Exception as exc:
        conn.rollback()
        raise db_error_to_http(exc)
    finally:
        conn.close()


# ======================= 4. NOTAS E PAGAMENTOS ==========================
@app.get("/api/notas")
def listar_notas():
    """NOTA_FISCAL + COMPRA, com total pago e saldo via functions."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT n.id_nota, n.numero, n.data_emissao, n.valor,
                   n.id_compra, f.nome AS fornecedor,
                   fn_total_pago_nota(n.id_nota) AS total_pago,
                   fn_saldo_nota(n.id_nota)      AS saldo
              FROM NOTA_FISCAL n
              JOIN COMPRA     c ON c.id_compra     = n.id_compra
              JOIN FORNECEDOR f ON f.id_fornecedor = c.id_fornecedor
             ORDER BY n.id_nota
        """)
        return cur.fetchall()


@app.post("/api/pagamentos", status_code=201)
def registrar_pagamento(p: PagamentoIn):
    """Chama sp_registrar_pagamento; trigger valida saldo da nota."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CALL sp_registrar_pagamento(%s, %s, %s, %s)",
                (p.id_nota, p.valor, p.forma_pagamento, p.data),
            )
        conn.commit()
        return {"mensagem": "Pagamento registrado com sucesso."}
    except Exception as exc:
        conn.rollback()
        raise db_error_to_http(exc)
    finally:
        conn.close()


# ========================== 5. RELATORIOS ===============================
@app.get("/api/relatorios/orcamentos")
def relatorio_orcamentos(ano: int = 2024):
    """Function sp_relatorio_orcamento: saldo e % consumido por orcamento."""
    with db_cursor() as cur:
        cur.execute("SELECT * FROM sp_relatorio_orcamento(%s)", (ano,))
        return cur.fetchall()


@app.get("/api/relatorios/fornecedores-top")
def relatorio_fornecedores_top():
    """Ranking de fornecedores que mais venderam (COMPRA + FORNECEDOR)."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT f.id_fornecedor, f.nome, f.regularidade_fiscal,
                   COUNT(c.id_compra) AS qtd_compras,
                   COALESCE(SUM(c.valor_total),0) AS total_vendido
              FROM FORNECEDOR f
              LEFT JOIN COMPRA c ON c.id_fornecedor = f.id_fornecedor
             GROUP BY f.id_fornecedor, f.nome, f.regularidade_fiscal
             HAVING COUNT(c.id_compra) > 0
             ORDER BY total_vendido DESC
        """)
        return cur.fetchall()


@app.get("/api/relatorios/orcamentos-consumo")
def relatorio_orcamentos_consumo():
    """Orcamentos ordenados por % consumido (ORCAMENTO + COMPRA)."""
    with db_cursor() as cur:
        cur.execute("""
            SELECT id_orcamento, ano, setor, projeto, valor_total, valor_consumido,
                   fn_saldo_orcamento(id_orcamento) AS saldo,
                   ROUND(valor_consumido / NULLIF(valor_total,0) * 100, 1) AS pct_consumido
              FROM ORCAMENTO
             ORDER BY pct_consumido DESC
        """)
        return cur.fetchall()
