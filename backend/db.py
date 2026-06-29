"""
Camada de acesso ao banco PostgreSQL (sugu_financeiro).

Usa psycopg2 com RealDictCursor (linhas como dicionarios). As credenciais
sao lidas de variaveis de ambiente (com defaults para o ambiente local:
usuario postgres em localhost:5432), permitindo configurar via arquivo
.env sem alterar o codigo.
"""
import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "dbname": os.getenv("DB_NAME", "sugu_financeiro"),
}


def get_connection():
    """Abre uma nova conexao com o banco (cursores retornam dicts)."""
    return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)


@contextmanager
def db_cursor(commit: bool = False):
    """
    Context manager que entrega um cursor pronto e cuida de
    commit/rollback e fechamento da conexao.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
