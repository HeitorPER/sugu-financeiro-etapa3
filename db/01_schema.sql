-- =====================================================================
-- SUGU - Subsistema Financeiro e de Compras
-- Etapa 2 - Esquema Fisico (schema, restricoes e indices)
-- SGBD: PostgreSQL 14+ - UTF-8
-- ---------------------------------------------------------------------
-- Execute conectado a um banco administrativo (ex.: "postgres"), pois
-- este script recria a base sugu_financeiro do zero:
--   psql -U postgres -f db/01_schema.sql
-- =====================================================================

DROP DATABASE IF EXISTS sugu_financeiro;
CREATE DATABASE sugu_financeiro WITH ENCODING 'UTF8';

\connect sugu_financeiro

-- ------------------------------- TABELAS -----------------------------
CREATE TABLE ORCAMENTO (
  id_orcamento     SERIAL PRIMARY KEY,
  ano              INT NOT NULL,
  valor_total      NUMERIC(15,2) NOT NULL DEFAULT 0.00,
  valor_consumido  NUMERIC(15,2) NOT NULL DEFAULT 0.00,
  setor            VARCHAR(100) NOT NULL,
  departamento     VARCHAR(100),
  projeto          VARCHAR(100),
  CONSTRAINT uq_orcamento  UNIQUE (ano, setor, departamento, projeto),
  CONSTRAINT chk_orc_ano   CHECK (ano BETWEEN 2000 AND 2100),
  CONSTRAINT chk_orc_valor CHECK (valor_total >= 0),
  CONSTRAINT chk_orc_consum CHECK (valor_consumido >= 0)
);

CREATE TABLE FORNECEDOR (
  id_fornecedor       SERIAL PRIMARY KEY,
  nome                VARCHAR(100) NOT NULL,
  cnpj                VARCHAR(18) NOT NULL,
  endereco            VARCHAR(150),
  telefone            VARCHAR(20),
  regularidade_fiscal VARCHAR(15) NOT NULL DEFAULT 'PENDENTE',
  CONSTRAINT uq_forn_cnpj UNIQUE (cnpj),
  CONSTRAINT chk_forn_cnpj CHECK (CHAR_LENGTH(cnpj) >= 14),
  CONSTRAINT chk_forn_reg  CHECK (regularidade_fiscal IN ('REGULAR','IRREGULAR','PENDENTE'))
);

CREATE TABLE LICITACAO (
  id_licitacao SERIAL PRIMARY KEY,
  tipo         VARCHAR(20) NOT NULL,
  nome         VARCHAR(120) NOT NULL,
  data_inicio  DATE NOT NULL,
  data_fim     DATE,
  status       VARCHAR(15) NOT NULL DEFAULT 'ABERTA',
  CONSTRAINT chk_lic_tipo   CHECK (tipo IN ('PREGAO','CONCORRENCIA','TOMADA_PRECO','CONVITE','DISPENSA')),
  CONSTRAINT chk_lic_status CHECK (status IN ('ABERTA','EM_ANALISE','HOMOLOGADA','CANCELADA','DESERTA')),
  CONSTRAINT chk_lic_datas  CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE PROPOSTA (
  id_proposta   SERIAL PRIMARY KEY,
  valor         NUMERIC(15,2) NOT NULL,
  data          DATE NOT NULL,
  vencedora     BOOLEAN NOT NULL DEFAULT FALSE,
  id_fornecedor INT NOT NULL,
  id_licitacao  INT NOT NULL,
  CONSTRAINT fk_prop_fornecedor FOREIGN KEY (id_fornecedor) REFERENCES FORNECEDOR(id_fornecedor),
  CONSTRAINT fk_prop_licitacao  FOREIGN KEY (id_licitacao)  REFERENCES LICITACAO(id_licitacao),
  CONSTRAINT uq_prop_forn_lic   UNIQUE (id_fornecedor, id_licitacao),
  CONSTRAINT chk_prop_valor     CHECK (valor > 0)
);

CREATE TABLE COMPRA (
  id_compra     SERIAL PRIMARY KEY,
  data          DATE NOT NULL,
  valor_total   NUMERIC(15,2) NOT NULL,
  id_fornecedor INT NOT NULL,
  id_licitacao  INT NULL,
  id_orcamento  INT NOT NULL,
  CONSTRAINT fk_compra_fornecedor FOREIGN KEY (id_fornecedor) REFERENCES FORNECEDOR(id_fornecedor),
  CONSTRAINT fk_compra_licitacao  FOREIGN KEY (id_licitacao)  REFERENCES LICITACAO(id_licitacao),
  CONSTRAINT fk_compra_orcamento  FOREIGN KEY (id_orcamento)  REFERENCES ORCAMENTO(id_orcamento),
  CONSTRAINT chk_compra_valor     CHECK (valor_total > 0)
);

CREATE TABLE NOTA_FISCAL (
  id_nota      SERIAL PRIMARY KEY,
  numero       VARCHAR(50) NOT NULL,
  data_emissao DATE NOT NULL,
  valor        NUMERIC(15,2) NOT NULL,
  id_compra    INT NOT NULL,
  CONSTRAINT fk_nota_compra FOREIGN KEY (id_compra) REFERENCES COMPRA(id_compra),
  CONSTRAINT uq_nota_numero UNIQUE (numero),
  CONSTRAINT chk_nota_valor CHECK (valor > 0)
);

CREATE TABLE PAGAMENTO (
  id_pagamento    SERIAL PRIMARY KEY,
  data            DATE NOT NULL,
  valor           NUMERIC(15,2) NOT NULL,
  forma_pagamento VARCHAR(15) NOT NULL DEFAULT 'TRANSFERENCIA',
  id_nota         INT NOT NULL,
  CONSTRAINT fk_pag_nota   FOREIGN KEY (id_nota) REFERENCES NOTA_FISCAL(id_nota),
  CONSTRAINT chk_pag_valor CHECK (valor > 0),
  CONSTRAINT chk_pag_forma CHECK (forma_pagamento IN ('TRANSFERENCIA','BOLETO','EMPENHO','PIX'))
);

CREATE TABLE PATRIMONIO (
  id_patrimonio      SERIAL PRIMARY KEY,
  descricao          VARCHAR(150) NOT NULL,
  localizacao        VARCHAR(100),
  estado_conservacao VARCHAR(15) NOT NULL DEFAULT 'NOVO',
  data_aquisicao     DATE NOT NULL,
  id_compra          INT NOT NULL,
  CONSTRAINT fk_patr_compra  FOREIGN KEY (id_compra) REFERENCES COMPRA(id_compra),
  CONSTRAINT chk_patr_estado CHECK (estado_conservacao IN ('NOVO','BOM','REGULAR','RUIM','INSERVIVEL'))
);

-- ------------------------------- INDICES -----------------------------
CREATE INDEX idx_fornecedor_nome    ON FORNECEDOR (nome);
CREATE INDEX idx_compra_data        ON COMPRA (data);
CREATE INDEX idx_nota_data_emissao  ON NOTA_FISCAL (data_emissao);
CREATE INDEX idx_licitacao_status   ON LICITACAO (status);
CREATE INDEX idx_patrimonio_estado  ON PATRIMONIO (estado_conservacao);
CREATE INDEX idx_compra_orc_forn    ON COMPRA (id_orcamento, id_fornecedor);
CREATE INDEX idx_proposta_lic_venc  ON PROPOSTA (id_licitacao, vencedora);
