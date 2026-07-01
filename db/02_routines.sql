-- =====================================================================
-- SUGU - Financeiro e de Compras - Functions, Triggers e Procedures
-- SGBD: PostgreSQL 14+ (PL/pgSQL)
-- Criadas ANTES da carga de dados, para que as triggers atuem na insercao.
-- =====================================================================

\connect sugu_financeiro

-- ============================ FUNCTIONS ==============================
CREATE OR REPLACE FUNCTION fn_saldo_orcamento(p_id_orcamento INT)
RETURNS NUMERIC(15,2) AS $$
DECLARE
  v_saldo NUMERIC(15,2);
BEGIN
  SELECT valor_total - valor_consumido INTO v_saldo
    FROM ORCAMENTO WHERE id_orcamento = p_id_orcamento;
  RETURN COALESCE(v_saldo, 0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_total_pago_nota(p_id_nota INT)
RETURNS NUMERIC(15,2) AS $$
DECLARE
  v_total NUMERIC(15,2);
BEGIN
  SELECT COALESCE(SUM(valor), 0) INTO v_total
    FROM PAGAMENTO WHERE id_nota = p_id_nota;
  RETURN v_total;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_saldo_nota(p_id_nota INT)
RETURNS NUMERIC(15,2) AS $$
DECLARE
  v_valor NUMERIC(15,2);
BEGIN
  SELECT valor INTO v_valor FROM NOTA_FISCAL WHERE id_nota = p_id_nota;
  RETURN COALESCE(v_valor, 0) - fn_total_pago_nota(p_id_nota);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_qtd_propostas(p_id_licitacao INT)
RETURNS INT AS $$
DECLARE
  v_qtd INT;
BEGIN
  SELECT COUNT(*) INTO v_qtd FROM PROPOSTA WHERE id_licitacao = p_id_licitacao;
  RETURN v_qtd;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_fornecedor_regular(p_id_fornecedor INT)
RETURNS BOOLEAN AS $$
DECLARE
  v_reg VARCHAR(15);
BEGIN
  SELECT regularidade_fiscal INTO v_reg
    FROM FORNECEDOR WHERE id_fornecedor = p_id_fornecedor;
  RETURN (v_reg = 'REGULAR');
END;
$$ LANGUAGE plpgsql;

-- ============================ TRIGGERS ===============================
-- No PostgreSQL cada trigger usa uma function que retorna TRIGGER.

CREATE OR REPLACE FUNCTION trgf_compra_before_insert()
RETURNS TRIGGER AS $$
DECLARE
  v_saldo NUMERIC(15,2);
BEGIN
  IF NOT fn_fornecedor_regular(NEW.id_fornecedor) THEN
    RAISE EXCEPTION 'Fornecedor sem regularidade fiscal: compra bloqueada.';
  END IF;
  v_saldo := fn_saldo_orcamento(NEW.id_orcamento);
  IF NEW.valor_total > v_saldo THEN
    RAISE EXCEPTION 'Saldo orcamentario insuficiente para a compra.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compra_before_insert
BEFORE INSERT ON COMPRA FOR EACH ROW
EXECUTE FUNCTION trgf_compra_before_insert();

CREATE OR REPLACE FUNCTION trgf_compra_after_insert()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE ORCAMENTO SET valor_consumido = valor_consumido + NEW.valor_total
    WHERE id_orcamento = NEW.id_orcamento;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compra_after_insert
AFTER INSERT ON COMPRA FOR EACH ROW
EXECUTE FUNCTION trgf_compra_after_insert();

CREATE OR REPLACE FUNCTION trgf_compra_after_delete()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE ORCAMENTO SET valor_consumido = valor_consumido - OLD.valor_total
    WHERE id_orcamento = OLD.id_orcamento;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compra_after_delete
AFTER DELETE ON COMPRA FOR EACH ROW
EXECUTE FUNCTION trgf_compra_after_delete();

CREATE OR REPLACE FUNCTION trgf_proposta_before_insert()
RETURNS TRIGGER AS $$
DECLARE
  v_status VARCHAR(15);
BEGIN
  SELECT status INTO v_status FROM LICITACAO WHERE id_licitacao = NEW.id_licitacao;
  IF v_status NOT IN ('ABERTA','EM_ANALISE') THEN
    RAISE EXCEPTION 'Licitacao nao esta aberta para receber propostas.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_proposta_before_insert
BEFORE INSERT ON PROPOSTA FOR EACH ROW
EXECUTE FUNCTION trgf_proposta_before_insert();

CREATE OR REPLACE FUNCTION trgf_pagamento_before_insert()
RETURNS TRIGGER AS $$
DECLARE
  v_saldo NUMERIC(15,2);
BEGIN
  v_saldo := fn_saldo_nota(NEW.id_nota);
  IF NEW.valor > v_saldo THEN
    RAISE EXCEPTION 'Pagamento excede o saldo em aberto da nota fiscal.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_pagamento_before_insert
BEFORE INSERT ON PAGAMENTO FOR EACH ROW
EXECUTE FUNCTION trgf_pagamento_before_insert();

CREATE OR REPLACE FUNCTION trgf_patrimonio_data()
RETURNS TRIGGER AS $$
DECLARE
  v_data_compra DATE;
BEGIN
  SELECT data INTO v_data_compra
    FROM COMPRA
   WHERE id_compra = NEW.id_compra;

  IF NEW.data_aquisicao < v_data_compra THEN
    RAISE EXCEPTION 'Data de aquisicao (%) e anterior a data da compra (%).',
      NEW.data_aquisicao, v_data_compra;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_patrimonio_data
BEFORE INSERT ON PATRIMONIO FOR EACH ROW
EXECUTE FUNCTION trgf_patrimonio_data();

-- ============================ PROCEDURES =============================
CREATE OR REPLACE PROCEDURE sp_registrar_compra(
  p_data DATE, p_valor NUMERIC(15,2), p_id_fornecedor INT,
  p_id_licitacao INT, p_id_orcamento INT, INOUT p_id_compra INT)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO COMPRA (data, valor_total, id_fornecedor, id_licitacao, id_orcamento)
  VALUES (p_data, p_valor, p_id_fornecedor, p_id_licitacao, p_id_orcamento)
  RETURNING id_compra INTO p_id_compra;
END;
$$;

CREATE OR REPLACE PROCEDURE sp_homologar_licitacao(p_id_licitacao INT, p_id_proposta INT)
LANGUAGE plpgsql AS $$
DECLARE
  v_existe INT;
BEGIN
  SELECT COUNT(*) INTO v_existe FROM PROPOSTA
    WHERE id_proposta = p_id_proposta AND id_licitacao = p_id_licitacao;
  IF v_existe = 0 THEN
    RAISE EXCEPTION 'Proposta informada nao pertence a esta licitacao.';
  END IF;
  UPDATE PROPOSTA SET vencedora = (id_proposta = p_id_proposta) WHERE id_licitacao = p_id_licitacao;
  UPDATE LICITACAO SET status = 'HOMOLOGADA' WHERE id_licitacao = p_id_licitacao;
END;
$$;
.
CREATE OR REPLACE PROCEDURE sp_registrar_pagamento(
  p_id_nota INT, p_valor NUMERIC(15,2), p_forma VARCHAR(15), p_data DATE)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO PAGAMENTO (data, valor, forma_pagamento, id_nota)
  VALUES (p_data, p_valor, p_forma, p_id_nota);
END;
$$;

-- Relatorio de orcamentos: no PostgreSQL um conjunto de resultados e
-- entregue de forma natural por uma function "table-valued".
CREATE OR REPLACE FUNCTION sp_relatorio_orcamento(p_ano INT)
RETURNS TABLE (
  id_orcamento    INT,
  setor           VARCHAR(100),
  projeto         VARCHAR(100),
  valor_total     NUMERIC(15,2),
  valor_consumido NUMERIC(15,2),
  saldo           NUMERIC(15,2),
  pct_consumido   NUMERIC
) AS $$
BEGIN
  RETURN QUERY
  SELECT o.id_orcamento, o.setor, o.projeto, o.valor_total, o.valor_consumido,
         fn_saldo_orcamento(o.id_orcamento) AS saldo,
         ROUND(o.valor_consumido / NULLIF(o.valor_total, 0) * 100, 1) AS pct_consumido
    FROM ORCAMENTO o
   WHERE o.ano = p_ano
   ORDER BY saldo ASC;
END;
$$ LANGUAGE plpgsql;
