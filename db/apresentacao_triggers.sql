-- =====================================================================
-- SUGU - Financeiro e de Compras  |  ETAPA DE APRESENTACAO
-- Parte 2: TRIGGERS NOVOS (um por aluno)
-- SGBD: PostgreSQL 14+
-- ---------------------------------------------------------------------
-- Rodar DEPOIS de 01/02/03. Cada trigger acompanha um bloco de teste
-- comentado (caso que PASSA e caso que e BLOQUEADO).
-- Rodar com:  psql -U postgres -d sugu_financeiro -f db/apresentacao_triggers.sql
-- =====================================================================
\connect sugu_financeiro

-- =====================================================================
-- ALUNO 1  -  Trigger em NOTA_FISCAL
-- Regra: a soma das notas de uma compra nao pode exceder o valor da compra.
-- =====================================================================
CREATE OR REPLACE FUNCTION trgf_nota_total_vs_compra()
RETURNS TRIGGER AS $$
DECLARE
  v_valor_compra NUMERIC(15,2);
  v_total_notas  NUMERIC(15,2);
BEGIN
  SELECT valor_total INTO v_valor_compra FROM COMPRA WHERE id_compra = NEW.id_compra;
  SELECT COALESCE(SUM(valor),0) INTO v_total_notas
    FROM NOTA_FISCAL WHERE id_compra = NEW.id_compra;
  IF v_total_notas + NEW.valor > v_valor_compra THEN
    RAISE EXCEPTION 'Total das notas (%) excede o valor da compra (%).',
      v_total_notas + NEW.valor, v_valor_compra;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_nota_total_vs_compra
BEFORE INSERT ON NOTA_FISCAL FOR EACH ROW
EXECUTE FUNCTION trgf_nota_total_vs_compra();

-- TESTE A1 (descomente para demonstrar):
-- CALL sp_registrar_compra('2025-08-01', 100000, 1, NULL, 1, NULL);  -- cria compra de 100000
-- INSERT INTO NOTA_FISCAL (numero, data_emissao, valor, id_compra)   -- PASSA (60000 <= 100000)
--   VALUES ('NF-DEMO-1', '2025-08-02', 60000, currval(pg_get_serial_sequence('compra','id_compra')));
-- INSERT INTO NOTA_FISCAL (numero, data_emissao, valor, id_compra)   -- FALHA (60000+50000 > 100000)
--   VALUES ('NF-DEMO-2','2025-08-03', 50000, currval(pg_get_serial_sequence('compra','id_compra')));


-- =====================================================================
-- ALUNO 2  -  Trigger em LICITACAO
-- Regra: uma licitacao HOMOLOGADA nao pode ter seu status revertido.
-- =====================================================================
CREATE OR REPLACE FUNCTION trgf_licitacao_status_imutavel()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.status = 'HOMOLOGADA' AND NEW.status <> 'HOMOLOGADA' THEN
    RAISE EXCEPTION 'Licitacao % ja homologada: status nao pode ser revertido.', OLD.id_licitacao;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_licitacao_status_imutavel
BEFORE UPDATE ON LICITACAO FOR EACH ROW
EXECUTE FUNCTION trgf_licitacao_status_imutavel();

-- TESTE A2 (descomente para demonstrar):
-- CALL sp_homologar_licitacao(1, 1);                                 -- PASSA: status vira HOMOLOGADA
-- UPDATE LICITACAO SET status = 'ABERTA' WHERE id_licitacao = 1;     -- FALHA: nao pode reverter


-- =====================================================================
-- ALUNO 3  -  Trigger em PATRIMONIO
-- Regra: data de aquisicao do bem nao pode ser anterior a data da compra.
-- =====================================================================
CREATE OR REPLACE FUNCTION trgf_patrimonio_data()
RETURNS TRIGGER AS $$
DECLARE
  v_data_compra DATE;
BEGIN
  SELECT data INTO v_data_compra FROM COMPRA WHERE id_compra = NEW.id_compra;
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

-- TESTE A3 (descomente para demonstrar):  compra 7 = 2025-03-05
-- INSERT INTO PATRIMONIO (descricao, localizacao, estado_conservacao, data_aquisicao, id_compra)
--   VALUES ('Gerador demo','Campus Norte','NOVO','2025-03-10', 7);  -- PASSA
-- INSERT INTO PATRIMONIO (descricao, localizacao, estado_conservacao, data_aquisicao, id_compra)
--   VALUES ('Item retroativo','Campus Norte','NOVO','2025-01-01', 7); -- FALHA


-- =====================================================================
-- ALUNO 4  -  Trigger em FORNECEDOR
-- Regra: normalizar dados na entrada (TRIM no nome, UPPER na regularidade).
-- Roda ANTES do CHECK, permitindo aceitar 'regular' e gravar 'REGULAR'.
-- =====================================================================
CREATE OR REPLACE FUNCTION trgf_fornecedor_normaliza()
RETURNS TRIGGER AS $$
BEGIN
  NEW.nome := TRIM(NEW.nome);
  NEW.regularidade_fiscal := UPPER(TRIM(NEW.regularidade_fiscal));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_fornecedor_normaliza
BEFORE INSERT OR UPDATE ON FORNECEDOR FOR EACH ROW
EXECUTE FUNCTION trgf_fornecedor_normaliza();

-- TESTE A4 (descomente para demonstrar):
-- INSERT INTO FORNECEDOR (nome, cnpj, regularidade_fiscal)
--   VALUES ('   Inovacoes Demo LTDA   ', '20.202.020/0001-20', 'regular')
--   RETURNING id_fornecedor, '['||nome||']' AS nome, regularidade_fiscal;  -- grava 'Inovacoes Demo LTDA' / 'REGULAR'
