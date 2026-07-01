-- =====================================================================
-- SUGU - Financeiro e de Compras - Carga de dados de teste (Etapa 2)
-- SGBD: PostgreSQL 14+
-- A ordem respeita as FKs e as regras das triggers. valor_consumido
-- nao e informado: e mantido automaticamente pela trigger de compra.
-- =====================================================================
\connect sugu_financeiro

INSERT INTO ORCAMENTO (id_orcamento, ano, valor_total, setor, departamento, projeto) VALUES
(1 ,2024,1500000.00,'Reitoria'                  ,'Administracao'    ,'Modernizacao Predial'),
(2 ,2024, 800000.00,'Biblioteca'                ,'Aquisicao Acervo' ,'Acervo Digital'),
(3 ,2024,1200000.00,'Departamento de Computacao','Laboratorios'     ,'Lab. de Redes'),
(4 ,2024, 600000.00,'Departamento de Fisica'    ,'Laboratorios'     ,'Lab. de Optica'),
(5 ,2025,2000000.00,'Reitoria'                  ,'Administracao'    ,'Obras Campus Norte'),
(6 ,2025, 950000.00,'Departamento de Computacao','Pesquisa'         ,'IA Aplicada'),
(7 ,2025, 500000.00,'Prefeitura Universitaria'  ,'Manutencao'       ,'Climatizacao'),
(8 ,2025, 750000.00,'Departamento de Quimica'   ,'Laboratorios'     ,'Reagentes'),
(9 ,2025,1100000.00,'Hospital Universitario'    ,'Equipamentos'     ,'UTI'),
(10,2025, 400000.00,'Departamento de Letras'    ,'Eventos'          ,'Congresso Anual'),
(11,2025, 300000.00,'Esporte'                   ,'Infraestrutura'   ,'Quadra Coberta'),
(12,2025,1800000.00,'TIC'                       ,'Infraestrutura'   ,'Datacenter');

-- ids 1-10 REGULAR, 11-13 PENDENTE, 14-15 IRREGULAR
INSERT INTO FORNECEDOR (id_fornecedor, nome, cnpj, endereco, telefone, regularidade_fiscal) VALUES
(1 ,'Tech Solutions LTDA'   ,'11.222.333/0001-44','Av. Sao Carlos, 1000' ,'(16) 3333-1000','REGULAR'),
(2 ,'Papelaria Central ME'  ,'22.333.444/0001-55','Rua XV, 234'          ,'(16) 3333-2000','REGULAR'),
(3 ,'Moveis Corporativos SA','33.444.555/0001-66','Av. Trabalhador, 500' ,'(16) 3333-3000','REGULAR'),
(4 ,'Optica Cientifica LTDA','44.555.666/0001-77','Rua das Flores, 89'   ,'(11) 4002-8922','REGULAR'),
(5 ,'Quimica Brasil LTDA'   ,'55.666.777/0001-88','Av. Industrial, 4500' ,'(11) 5555-1212','REGULAR'),
(6 ,'Refrigeracao Polar SA' ,'66.777.888/0001-99','Rua Gelada, 12'       ,'(16) 3333-4000','REGULAR'),
(7 ,'Construtora Norte LTDA','77.888.999/0001-00','Av. Obras, 3000'      ,'(16) 3333-5000','REGULAR'),
(8 ,'MedEquip Hospitalar SA','88.999.000/0001-11','Rua Saude, 700'       ,'(11) 3030-7070','REGULAR'),
(9 ,'Eventos & Cia LTDA'    ,'99.000.111/0001-22','Av. Festas, 45'       ,'(16) 3333-6000','REGULAR'),
(10,'DataCenter Infra LTDA' ,'10.111.222/0001-33','Av. Servidores, 9'    ,'(11) 4004-9090','REGULAR'),
(11,'Suprimentos Rapidos ME','12.121.212/0001-12','Rua do Comercio, 33'  ,'(16) 3333-7000','PENDENTE'),
(12,'Limpeza Total LTDA'    ,'13.131.313/0001-13','Av. Higiene, 220'     ,'(16) 3333-8000','PENDENTE'),
(13,'Grafica Express ME'    ,'14.141.414/0001-14','Rua Tinta, 5'         ,'(16) 3333-9000','PENDENTE'),
(14,'Materiais Diversos SA' ,'15.151.515/0001-15','Av. Atrasada, 1'      ,'(11) 2002-0202','IRREGULAR'),
(15,'Servicos Gerais ME'    ,'16.161.616/0001-16','Rua Pendencia, 7'     ,'(11) 2003-0303','IRREGULAR');

INSERT INTO LICITACAO (id_licitacao, tipo, nome, data_inicio, data_fim, status) VALUES
(1 ,'PREGAO'      ,'Aquisicao de servidores de rack'          ,'2024-01-10','2024-02-10','ABERTA'),
(2 ,'CONCORRENCIA','Fornecimento de material de escritorio'   ,'2024-02-01','2024-03-15','ABERTA'),
(3 ,'PREGAO'      ,'Aquisicao de estantes para acervo'        ,'2024-02-20','2024-03-20','ABERTA'),
(4 ,'CONVITE'     ,'Servicos de climatizacao'                 ,'2024-03-05','2024-03-25','ABERTA'),
(5 ,'CONCORRENCIA','Reforma de laboratorio de pesquisa'       ,'2025-01-15','2025-03-01','ABERTA'),
(6 ,'PREGAO'      ,'Aquisicao de equipamentos de informatica' ,'2025-02-10','2025-03-10','ABERTA'),
(7 ,'TOMADA_PRECO','Obra de estrutura metalica'               ,'2025-02-15','2025-03-20','ABERTA'),
(8 ,'PREGAO'      ,'Aquisicao de licencas de software'        ,'2025-03-01','2025-04-01','ABERTA'),
(9 ,'CONVITE'     ,'Servicos de manutencao predial'           ,'2025-03-10','2025-03-30','ABERTA'),
(10,'CONCORRENCIA','Infraestrutura de data center'            ,'2025-03-20','2025-05-10','ABERTA'),
(11,'PREGAO'      ,'Aquisicao de mobiliario corporativo'      ,'2025-04-01','2025-04-30','ABERTA'),
(12,'DISPENSA'    ,'Contratacao emergencial de suprimentos'   ,'2025-04-05','2025-04-15','ABERTA');

INSERT INTO PROPOSTA (id_proposta, valor, data, id_fornecedor, id_licitacao) VALUES
(1 , 48000.00,'2024-01-15', 1, 1),
(2 , 51000.00,'2024-01-16', 3, 1),
(3 , 44000.00,'2024-02-05', 2, 2),
(4 ,118000.00,'2024-02-07', 4, 2),
(5 , 60000.00,'2024-02-25', 5, 3),
(6 , 58000.00,'2024-02-26', 1, 3),
(7 , 80000.00,'2024-03-08', 6, 4),
(8 , 39000.00,'2024-03-09', 2, 4),
(9 ,250000.00,'2025-01-20', 7, 5),
(10,265000.00,'2025-01-22', 8, 5),
(11, 90000.00,'2025-02-12', 9, 6),
(12, 95000.00,'2025-02-13',10, 6),
(13,110000.00,'2025-02-20',11, 7),
(14,300000.00,'2025-03-05',12, 8),
(15, 95000.00,'2025-03-12',13, 9),
(16,500000.00,'2025-03-25',14,10),
(17, 28000.00,'2025-04-03', 2,11),
(18, 42000.00,'2025-04-06', 3,12);

-- somente fornecedores REGULARES; saldo validado por trigger
INSERT INTO COMPRA (id_compra, data, valor_total, id_fornecedor, id_licitacao, id_orcamento) VALUES
(1 ,'2024-02-12', 50000.00, 1, 1 , 1),
(2 ,'2024-02-15', 30000.00, 2, NULL, 1),
(3 ,'2024-03-18', 45000.00, 3, 2 , 2),
(4 ,'2024-03-22',120000.00, 4, 3 , 3),
(5 ,'2024-03-25', 60000.00, 5, NULL, 3),
(6 ,'2024-03-28', 80000.00, 6, 4 , 4),
(7 ,'2025-03-05',250000.00, 7, 5 , 5),
(8 ,'2025-03-12', 90000.00, 8, 6 , 6),
(9 ,'2025-03-15', 70000.00, 9, NULL, 7),
(10,'2025-03-22',110000.00,10, 7 , 8),
(11,'2025-03-30',300000.00, 1, 8 , 9),
(12,'2025-04-02', 40000.00, 2, NULL,10),
(13,'2025-04-05', 95000.00, 3, 9 ,11),
(14,'2025-05-12',500000.00, 4,10 ,12),
(15,'2025-05-15',200000.00, 5, NULL,12);

-- compra 1 possui 2 notas (1:N)
INSERT INTO NOTA_FISCAL (id_nota, numero, data_emissao, valor, id_compra) VALUES
(1 ,'NF-2024-0001','2024-02-12', 30000.00, 1),
(2 ,'NF-2024-0002','2024-02-15', 30000.00, 2),
(3 ,'NF-2024-0003','2024-03-18', 45000.00, 3),
(4 ,'NF-2024-0004','2024-03-22',120000.00, 4),
(5 ,'NF-2024-0005','2024-03-25', 60000.00, 5),
(6 ,'NF-2024-0006','2024-03-28', 80000.00, 6),
(7 ,'NF-2025-0007','2025-03-05',250000.00, 7),
(8 ,'NF-2025-0008','2025-03-12', 90000.00, 8),
(9 ,'NF-2025-0009','2025-03-15', 70000.00, 9),
(10,'NF-2025-0010','2025-03-22',110000.00,10),
(11,'NF-2025-0011','2025-03-30',300000.00,11),
(12,'NF-2025-0012','2025-04-02', 40000.00,12),
(13,'NF-2025-0013','2025-04-05', 95000.00,13),
(14,'NF-2025-0014','2025-05-12',500000.00,14),
(15,'NF-2024-0015','2024-02-20', 20000.00, 1);

INSERT INTO PAGAMENTO (id_pagamento, data, valor, forma_pagamento, id_nota) VALUES
(1 ,'2024-03-01', 30000.00,'EMPENHO'      , 1),
(2 ,'2024-03-05', 15000.00,'TRANSFERENCIA', 2),
(3 ,'2024-04-01', 45000.00,'BOLETO'       , 3),
(4 ,'2024-04-10', 60000.00,'TRANSFERENCIA', 4),
(5 ,'2024-04-20', 60000.00,'TRANSFERENCIA', 4),
(6 ,'2024-04-15', 60000.00,'PIX'          , 5),
(7 ,'2024-04-18', 80000.00,'EMPENHO'      , 6),
(8 ,'2025-04-01',100000.00,'TRANSFERENCIA', 7),
(9 ,'2025-04-05', 90000.00,'BOLETO'       , 8),
(10,'2025-04-12',110000.00,'EMPENHO'      ,10),
(11,'2025-04-20',150000.00,'TRANSFERENCIA',11),
(12,'2025-05-01', 40000.00,'PIX'          ,12),
(13,'2025-05-05', 95000.00,'BOLETO'       ,13),
(14,'2025-06-01',250000.00,'EMPENHO'      ,14),
(15,'2024-03-10', 20000.00,'PIX'          ,15);

INSERT INTO PATRIMONIO (id_patrimonio, descricao, localizacao, estado_conservacao, data_aquisicao, id_compra) VALUES
(1 ,'Servidor de rack Dell'         ,'Datacenter - Sala 1'     ,'NOVO'    ,'2024-02-12', 1),
(2 ,'Lote de cadeiras de escritorio','Reitoria - 2 andar'      ,'NOVO'    ,'2024-02-15', 2),
(3 ,'Estantes para acervo'          ,'Biblioteca - Terreo'     ,'BOM'     ,'2024-03-18', 3),
(4 ,'Bancada optica anti-vibracao'  ,'Lab. Optica - Fisica'    ,'NOVO'    ,'2024-03-22', 4),
(5 ,'Capela de exaustao quimica'    ,'Lab. Quimica'            ,'NOVO'    ,'2024-03-25', 5),
(6 ,'Sistema de ar-condicionado'    ,'Bloco A - Sala 101'      ,'BOM'     ,'2024-03-28', 6),
(7 ,'Estrutura metalica de obra'    ,'Campus Norte'            ,'NOVO'    ,'2025-03-05', 7),
(8 ,'Cluster de GPUs para IA'       ,'Lab. de Computacao'      ,'NOVO'    ,'2025-03-12', 8),
(9 ,'Conjunto de climatizadores'    ,'Prefeitura Universitaria','REGULAR' ,'2025-03-15', 9),
(10,'Switches de rede gerenciaveis' ,'Datacenter - Sala 2'     ,'NOVO'    ,'2025-03-22',10),
(11,'Mobiliario administrativo'     ,'Hospital - Ala UTI'      ,'BOM'     ,'2025-03-30',11),
(12,'Material grafico congresso'    ,'Dep. Letras'             ,'REGULAR' ,'2025-04-02',12),
(13,'Equipamento de laboratorio'    ,'Esporte - Quadra'        ,'BOM'     ,'2025-04-05',13),
(14,'Storage de alta capacidade'    ,'Datacenter - Sala 3'     ,'NOVO'    ,'2025-05-12',14),
(15,'Nobreak industrial'            ,'Datacenter - Sala 3'     ,'NOVO'    ,'2025-05-15',15);

UPDATE LICITACAO SET status = 'EM_ANALISE' WHERE id_licitacao IN (5, 6);
UPDATE LICITACAO SET status = 'CANCELADA'  WHERE id_licitacao = 11;
UPDATE LICITACAO SET status = 'DESERTA'    WHERE id_licitacao = 12;

-- ---------------------------------------------------------------------
-- Como os ids foram inseridos explicitamente, e preciso avancar as
-- sequences (SERIAL) para o proximo valor, senao novos INSERTs feitos
-- pela API colidiriam com os ids da carga.
-- ---------------------------------------------------------------------
SELECT setval(pg_get_serial_sequence('orcamento','id_orcamento'),     (SELECT MAX(id_orcamento)  FROM ORCAMENTO));
SELECT setval(pg_get_serial_sequence('fornecedor','id_fornecedor'),   (SELECT MAX(id_fornecedor) FROM FORNECEDOR));
SELECT setval(pg_get_serial_sequence('licitacao','id_licitacao'),     (SELECT MAX(id_licitacao)  FROM LICITACAO));
SELECT setval(pg_get_serial_sequence('proposta','id_proposta'),       (SELECT MAX(id_proposta)   FROM PROPOSTA));
SELECT setval(pg_get_serial_sequence('compra','id_compra'),           (SELECT MAX(id_compra)     FROM COMPRA));
SELECT setval(pg_get_serial_sequence('nota_fiscal','id_nota'),        (SELECT MAX(id_nota)       FROM NOTA_FISCAL));
SELECT setval(pg_get_serial_sequence('pagamento','id_pagamento'),     (SELECT MAX(id_pagamento)  FROM PAGAMENTO));
SELECT setval(pg_get_serial_sequence('patrimonio','id_patrimonio'),   (SELECT MAX(id_patrimonio) FROM PATRIMONIO));
