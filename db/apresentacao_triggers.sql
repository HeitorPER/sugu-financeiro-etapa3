-- =====================================================================
-- SUGU - Financeiro e de Compras - Triggers da Apresentacao
-- SGBD: PostgreSQL 14+ (PL/pgSQL)
-- Cada trigger acompanha um bloco de teste comentado.
-- Execute APOS 01_schema.sql, 02_routines.sql e 03_seed.sql:
--   psql -U postgres -f db/apresentacao_triggers.sql
-- =====================================================================

\connect sugu_financeiro

-- ---------------------------------------------------------------------
-- Aluno 2 - Licitacoes
-- Parte 2 - Trigger - LICITACAO (status HOMOLOGADA e imutavel)
-- Regra: uma licitacao ja HOMOLOGADA nao pode ter seu status revertido.
-- BEFORE UPDATE: compara OLD.status (valor antigo) com NEW.status (valor
-- que se tenta gravar); se ja estava homologada e tentam mudar para outro
-- estado, a operacao e bloqueada - garante a integridade do processo.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trgf_licitacao_status_imutavel()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.status = 'HOMOLOGADA' AND NEW.status <> 'HOMOLOGADA' THEN
    RAISE EXCEPTION 'Licitacao % ja homologada: status nao pode ser revertido.', OLD.id_licitacao;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_licitacao_status_imutavel ON LICITACAO;
CREATE TRIGGER trg_licitacao_status_imutavel
BEFORE UPDATE ON LICITACAO FOR EACH ROW
EXECUTE FUNCTION trgf_licitacao_status_imutavel();

-- Bloco de teste (descomente para demonstrar):
-- CALL sp_homologar_licitacao(1, 1);                              -- PASSA
-- SELECT id_licitacao, status FROM LICITACAO WHERE id_licitacao = 1;
-- --> 1 | HOMOLOGADA
-- UPDATE LICITACAO SET status = 'ABERTA' WHERE id_licitacao = 1;  -- FALHA
-- --> ERROR:  Licitacao 1 ja homologada: status nao pode ser revertido.
