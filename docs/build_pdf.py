# -*- coding: utf-8 -*-
"""Gera o PDF de entrega da Etapa 3 (10 itens)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Image as RLImage
from PIL import Image as PILImage

HERE = os.path.dirname(__file__)
PRINTS = os.path.join(HERE, "prints")
OUT = os.path.join(HERE, "Etapa3_Financeiro_Compras.pdf")

BRAND = colors.HexColor("#1d4ed8")
INK = colors.HexColor("#0f172a")
MUTED = colors.HexColor("#475569")
LINE = colors.HexColor("#cbd5e1")
SOFT = colors.HexColor("#eff6ff")

styles = getSampleStyleSheet()
def style(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

H1 = style("H1", fontSize=18, leading=22, textColor=INK, spaceAfter=4, fontName="Helvetica-Bold")
SUB = style("SUB", fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=2)
H2 = style("H2", fontSize=13.5, leading=17, textColor=BRAND, spaceBefore=14, spaceAfter=7, fontName="Helvetica-Bold")
H3 = style("H3", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3, fontName="Helvetica-Bold")
BODY = style("BODY", fontSize=10.3, leading=15, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6)
SMALL = style("SMALL", fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=12)
NOTE = style("NOTE", fontSize=8.8, leading=12, textColor=MUTED, alignment=TA_LEFT, spaceAfter=4)
LI = style("LI", fontSize=10.3, leading=14.5, textColor=INK, alignment=TA_JUSTIFY)
CODE = style("CODE", fontSize=8.6, leading=11, textColor=colors.HexColor("#0f172a"),
             fontName="Courier", backColor=colors.HexColor("#f1f5f9"))
CELL = style("CELL", fontSize=9.2, leading=12.5, textColor=INK, alignment=TA_LEFT)

CELLH = style("CELLH", fontSize=9.4, leading=12.5, textColor=colors.white,
              alignment=TA_LEFT, fontName="Helvetica-Bold")

def P(txt):
    """Célula de tabela que quebra linha."""
    return Paragraph(txt, CELL)

def PH(txt):
    """Célula de cabeçalho (texto branco)."""
    return Paragraph(f"<b>{txt}</b>", CELLH)

story = []

def img_fit(path, max_w=16.4 * cm, max_h=20 * cm, caption=None):
    iw, ih = PILImage.open(path).size
    ratio = min(max_w / iw, max_h / ih)
    im = RLImage(path, width=iw * ratio, height=ih * ratio)
    im.hAlign = "CENTER"
    flow = [im]
    if caption:
        flow.append(Spacer(1, 3))
        flow.append(Paragraph(caption, SMALL))
    return KeepTogether(flow)

def hr():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=4, spaceAfter=10)

# ============================== CAPA / CABECALHO ==========================
story.append(Paragraph("Projeto de Banco de Dados — Etapa 3", H1))
story.append(Paragraph("Acesso ao banco de dados via aplicação (Python + React)", SUB))
story.append(hr())

# ---------------------------------- ITEM 1 -------------------------------
story.append(Paragraph("1. Grupo e integrantes", H2))
story.append(Paragraph("Grupo nº: <b>____</b> &nbsp;&nbsp;(preencher com o número do grupo)", BODY))
integrantes = [
    ["Integrante (ordem alfabética)", "RA"],
    ["Daniel Gidrão", "829511"],
    ["Gustavo Bragaia", "834383"],
    ["Heitor Giometti", "834220"],
    ["Lucas Martinez", "832627"],
]
t = Table(integrantes, colWidths=[11 * cm, 5 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
]))
story.append(t)

# ---------------------------------- ITEM 2 -------------------------------
story.append(Paragraph("2. Título do subsistema", H2))
story.append(Paragraph(
    "<b>Gestão Financeira e de Compras da Universidade</b> — subsistema do SUGU "
    "(Sistema Unificado de Gestão Universitária). Abrange orçamentos por setor/projeto, "
    "fornecedores e sua regularidade fiscal, licitações e propostas, efetivação de compras, "
    "notas fiscais, pagamentos e patrimônio adquirido.", BODY))

# ---------------------------------- ITEM 3 -------------------------------
story.append(Paragraph("3. DER final (Etapa 1/2)", H2))
story.append(Paragraph(
    "Diagrama Entidade-Relacionamento (notação de Chen) entregue nas etapas anteriores, "
    "com as oito entidades e os relacionamentos do subsistema.", BODY))
story.append(img_fit(os.path.join(PRINTS, "der.png"),
                     caption="Figura 1 — DER do subsistema Financeiro e de Compras."))

# ---------------------------------- ITEM 4 -------------------------------
story.append(Paragraph("4. Esquema Relacional final", H2))
story.append(Paragraph(
    "Mapeamento relacional (notação pé-de-galinha) com as oito tabelas, chaves primárias (PK), "
    "estrangeiras (FK) e restrições de unicidade (UQ).", BODY))
story.append(img_fit(os.path.join(PRINTS, "relacional.png"),
                     caption="Figura 2 — Esquema Relacional do subsistema."))

story.append(PageBreak())

# ---------------------------------- ITEM 5 -------------------------------
story.append(Paragraph("5. Funcionalidades implementadas", H2))
story.append(Paragraph(
    "Todas as funcionalidades acessam o banco da Etapa 2 e envolvem 2 ou mais entidades e "
    "pelo menos um relacionamento, reutilizando as <i>functions</i>, <i>triggers</i> e "
    "<i>procedures</i> já definidas. A lista a seguir descreve cada operação e as tabelas envolvidas:", BODY))

func_items = [
    ("a) Cadastro de fornecedores",
     "Cadastra novos fornecedores com seus dados e regularidade fiscal. "
     "<b>INSERÇÃO</b> na tabela FORNECEDOR (restrições UNIQUE de CNPJ e CHECK de regularidade)."),
    ("b) Atualização de regularidade fiscal",
     "Altera a situação fiscal de um fornecedor (REGULAR/PENDENTE/IRREGULAR). "
     "<b>ATUALIZAÇÃO</b> na tabela FORNECEDOR — afeta diretamente a regra de compras."),
    ("c) Efetuar compra",
     "Registra uma compra vinculada a um fornecedor e a um orçamento. "
     "<b>Seleção</b> em FORNECEDOR e ORCAMENTO; <b>chamada</b> da procedure "
     "<font name='Courier'>sp_registrar_compra()</font>; <b>inserção</b> em COMPRA. "
     "As triggers <font name='Courier'>trg_compra_before_insert</font> (functions "
     "<font name='Courier'>fn_fornecedor_regular</font> e <font name='Courier'>fn_saldo_orcamento</font>) "
     "e <font name='Courier'>trg_compra_after_insert</font> (atualiza ORCAMENTO.valor_consumido) atuam aqui."),
    ("d) Registrar proposta em licitação",
     "Adiciona a proposta de um fornecedor a uma licitação. <b>Inserção</b> em PROPOSTA; "
     "<b>consulta</b> em FORNECEDOR e LICITACAO. A trigger "
     "<font name='Courier'>trg_proposta_before_insert</font> só permite licitações abertas."),
    ("e) Homologar licitação",
     "Define a proposta vencedora e encerra o certame. <b>Chamada</b> da procedure "
     "<font name='Courier'>sp_homologar_licitacao()</font> — <b>atualiza</b> PROPOSTA (vencedora) e LICITACAO (status)."),
    ("f) Registrar pagamento de nota fiscal",
     "Registra pagamentos de uma nota fiscal. <b>Chamada</b> de "
     "<font name='Courier'>sp_registrar_pagamento()</font>; <b>inserção</b> em PAGAMENTO; "
     "<b>consulta</b> em NOTA_FISCAL. A trigger <font name='Courier'>trg_pagamento_before_insert</font> "
     "(function <font name='Courier'>fn_saldo_nota</font>) impede pagar acima do saldo em aberto."),
    ("g) Relatório de orçamentos",
     "Relatório gerencial com saldo e % consumido por orçamento. <b>Chamada</b> da procedure "
     "<font name='Courier'>sp_relatorio_orcamento()</font> sobre ORCAMENTO (function "
     "<font name='Courier'>fn_saldo_orcamento</font>)."),
    ("h) Ranking de fornecedores que mais venderam",
     "Relatório gerencial agregando o total comprado por fornecedor. "
     "<b>Consulta</b> com JOIN entre COMPRA e FORNECEDOR (relacionamento <i>realiza</i>)."),
    ("i) Painel financeiro (dashboard)",
     "Indicadores consolidados (fornecedores, compras, saldo total, licitações abertas). "
     "<b>Consultas</b> agregadas em FORNECEDOR, COMPRA, ORCAMENTO e LICITACAO."),
]
story.append(ListFlowable(
    [ListItem(Paragraph(f"<b>{t}.</b> {d}", LI), value=None) for t, d in func_items],
    bulletType="bullet", start="square", leftIndent=14, spaceBefore=2,
))

# ---------------------------------- ITEM 6 -------------------------------
story.append(Paragraph("6. Tecnologias utilizadas", H2))
tech = [
    [PH("Tecnologia"), PH("Para que foi usada")],
    [P("<b>Python 3.13</b>"), P("Linguagem de acesso ao banco (back-end), conforme exigido pelo exercício.")],
    [P("<b>FastAPI</b>"), P("Framework que expõe as funcionalidades como uma API REST (endpoints /api/...).")],
    [P("<b>Uvicorn</b>"), P("Servidor ASGI que executa a aplicação FastAPI.")],
    [P("<b>PyMySQL</b>"), P("Driver de conexão Python para MariaDB; executa SQL, procedures e functions.")],
    [P("<b>python-dotenv</b>"), P("Lê as credenciais do banco de um arquivo .env (configuração sem hard-code).")],
    [P("<b>React 18 + Vite</b>"), P("Front-end (SPA) com as telas das funcionalidades; proxy /api para o back-end.")],
    [P("<b>MariaDB 10.11</b>"), P("SGBD do subsistema (banco sugu_financeiro criado na Etapa 2).")],
    [P("<b>Docker</b>"), P("Provisiona o container do MariaDB 10.11, garantindo fidelidade ao ambiente da Etapa 2.")],
    [P("<b>Playwright</b>"), P("Automação do navegador para capturar os prints das telas (Seção 7).")],
]
tt = Table(tech, colWidths=[4.4 * cm, 11.6 * cm])
tt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.3),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(tt)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "<b>Arquitetura:</b> o navegador (React) chama a API em Python (FastAPI), que se conecta ao "
    "MariaDB via PyMySQL e dispara as procedures/triggers do banco — exatamente o ciclo "
    "“aplicação → linguagem de programação → banco de dados” pedido no enunciado.", BODY))

story.append(PageBreak())

# ---------------------------------- ITEM 7 -------------------------------
story.append(Paragraph("7. Telas da aplicação (prints)", H2))
shots = [
    ("01_dashboard.png", "Painel Financeiro",
     "Tela inicial com indicadores consolidados e o consumo de cada orçamento "
     "(barras de progresso). Agrega dados de FORNECEDOR, COMPRA, ORCAMENTO e LICITACAO."),
    ("02_fornecedores.png", "Fornecedores",
     "Cadastro de novo fornecedor (formulário) e listagem com a regularidade fiscal de cada um, "
     "que pode ser alterada. Operações de INSERT e UPDATE na tabela FORNECEDOR."),
    ("03_compras.png", "Efetuar Compra",
     "Formulário para registrar uma compra escolhendo fornecedor, orçamento e (opcionalmente) "
     "licitação, exibindo o saldo disponível. Aciona a procedure sp_registrar_compra e as triggers."),
    ("07_compra_bloqueada.png", "Efetuar Compra — regra de negócio",
     "Demonstração da trigger: ao tentar comprar de um fornecedor IRREGULAR, o banco bloqueia a "
     "operação (SIGNAL 45000) e a aplicação exibe a mensagem “Fornecedor sem regularidade fiscal: "
     "compra bloqueada.”"),
    ("04_licitacoes.png", "Licitações e Propostas",
     "Lista de licitações com o nº de propostas (function fn_qtd_propostas). Ao abrir uma licitação, "
     "mostra as propostas (PROPOSTA + FORNECEDOR), permite registrar nova proposta e homologar "
     "(procedure sp_homologar_licitacao)."),
    ("05_pagamentos.png", "Pagamentos de Notas",
     "Registro de pagamentos das notas fiscais com saldo em aberto calculado (functions "
     "fn_total_pago_nota e fn_saldo_nota). A trigger impede pagamento acima do saldo."),
    ("06_relatorios.png", "Relatórios Gerenciais",
     "Relatório de saldo dos orçamentos por ano (procedure sp_relatorio_orcamento) e ranking de "
     "fornecedores que mais venderam (JOIN COMPRA + FORNECEDOR)."),
]
for i, (fn, title, desc) in enumerate(shots, 1):
    story.append(Paragraph(f"7.{i} — {title}", H3))
    story.append(Paragraph(desc, BODY))
    story.append(img_fit(os.path.join(PRINTS, fn), max_h=12.5 * cm))
    story.append(Spacer(1, 10))

story.append(PageBreak())

# ---------------------------------- ITEM 8 -------------------------------
story.append(Paragraph("8. Entrega da aplicação", H2))
story.append(Paragraph(
    "<b>Código-fonte (repositório):</b> "
    "<font color='#1d4ed8'>https://github.com/danielgidrao/sugu-financeiro-etapa3</font>", BODY))
story.append(Paragraph(
    "<b>Vídeo demonstrativo (3 min):</b> "
    "<font color='#1d4ed8'>&lt;inserir link do vídeo&gt;</font>.", BODY))
story.append(Paragraph(
    "O repositório contém: <font name='Courier'>db/</font> (scripts SQL da Etapa 2 — schema, "
    "rotinas e carga), <font name='Courier'>backend/</font> (API FastAPI em Python) e "
    "<font name='Courier'>frontend/</font> (aplicação React/Vite), além do <font name='Courier'>README.md</font> "
    "com as instruções de execução.", BODY))

# ---------------------------------- ITEM 9 -------------------------------
story.append(Paragraph("9. Dificuldades enfrentadas e soluções", H2))
difs = [
    ("Procedure com parâmetro de saída (OUT)",
     "A <font name='Courier'>sp_registrar_compra</font> retorna o id da compra por um parâmetro OUT, "
     "que o PyMySQL não devolve diretamente. <b>Solução:</b> chamar "
     "<font name='Courier'>CALL ...(@novo_id)</font> e, na mesma conexão, executar "
     "<font name='Courier'>SELECT @novo_id</font>."),
    ("Diretiva DELIMITER na carga do banco",
     "O PyMySQL executa um comando por vez e não entende a diretiva DELIMITER usada para criar "
     "triggers/procedures. <b>Solução:</b> carregar os scripts pelo cliente nativo "
     "<font name='Courier'>mariadb</font> (no container), e usar o PyMySQL apenas para as operações da aplicação."),
    ("Traduzir erros do banco para o usuário",
     "Triggers (SIGNAL 45000), CHECK, UNIQUE e FK retornam erros técnicos. <b>Solução:</b> uma camada "
     "de tratamento converte essas exceções em respostas HTTP 400 com a mensagem de negócio, exibida na tela."),
    ("CORS entre front-end e back-end",
     "React (porta 5173) e API (porta 8000) em origens diferentes. <b>Solução:</b> proxy "
     "<font name='Courier'>/api</font> no Vite e <font name='Courier'>CORSMiddleware</font> no FastAPI."),
    ("Banco não instalado na máquina",
     "Não havia MariaDB local. <b>Solução:</b> subir o MariaDB 10.11 em um container Docker e recarregar "
     "os scripts da Etapa 2, preservando restrições, índices, functions, triggers e procedures."),
]
story.append(ListFlowable(
    [ListItem(Paragraph(f"<b>{t}.</b> {d}", LI)) for t, d in difs],
    bulletType="bullet", start="square", leftIndent=14,
))

# ---------------------------------- ITEM 10 ------------------------------
story.append(PageBreak())
story.append(Paragraph("10. Contribuição individual", H2))
story.append(Paragraph(
    "Cada integrante foi responsável por uma funcionalidade de ponta a ponta — do banco de dados "
    "e do back-end (Python) até a respectiva tela no front-end (React) — dividindo o trabalho de "
    "forma equilibrada (links dos vídeos individuais a inserir):", BODY))
contrib = [
    [PH("Integrante"), PH("RA"), PH("Tarefas realizadas (do banco ao front)")],
    [P("<b>Daniel Gidrão</b>"), P("829511"),
     P("<b>Relatórios e Painel.</b> No banco: consultas analíticas e a procedure "
       "<font name='Courier'>sp_relatorio_orcamento</font> (com a function "
       "<font name='Courier'>fn_saldo_orcamento</font>). No back-end: endpoints de relatórios e do "
       "dashboard. No front: telas de <i>Relatórios</i> e <i>Painel Financeiro</i>.")],
    [P("<b>Gustavo Bragaia</b>"), P("834383"),
     P("<b>Fornecedores.</b> No banco: tabela FORNECEDOR e suas restrições (UNIQUE de CNPJ e CHECK "
       "de regularidade). No back-end: endpoints de cadastro e de atualização da regularidade fiscal. "
       "No front: tela de <i>Fornecedores</i>.")],
    [P("<b>Heitor Giometti</b>"), P("834220"),
     P("<b>Compras.</b> No banco: procedure <font name='Courier'>sp_registrar_compra</font> e as "
       "triggers de compra/orçamento (regularidade, saldo e consumo). No back-end: endpoint de efetuar "
       "compra. No front: tela <i>Efetuar Compra</i>, com a demonstração das regras de negócio.")],
    [P("<b>Lucas Martinez</b>"), P("832627"),
     P("<b>Licitações, Propostas e Pagamentos.</b> No banco: procedures "
       "<font name='Courier'>sp_homologar_licitacao</font> e <font name='Courier'>sp_registrar_pagamento</font> "
       "e as triggers de proposta/pagamento. No back-end: endpoints correspondentes. No front: telas de "
       "<i>Licitações</i> e <i>Pagamentos</i>.")],
]
ct = Table(contrib, colWidths=[3.2 * cm, 1.8 * cm, 11 * cm])
ct.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), BRAND),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (1, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.2),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(ct)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "<i>Base comum (provisão do MariaDB 10.11 em Docker, camada de acesso a dados em "
    "<font name='Courier'>db.py</font>, padronização do tratamento de erros da API e a navegação/estilos "
    "do front-end) desenvolvida em conjunto pelos quatro integrantes.</i>", NOTE))

# ------------------------------- RENDER ----------------------------------
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.4 * cm, rightMargin=2.4 * cm,
    topMargin=2 * cm, bottomMargin=1.8 * cm,
    title="Etapa 3 - Financeiro e Compras (SUGU)",
)

def footer(canvas, d):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2.4 * cm, 1 * cm, "SUGU — Financeiro e de Compras · Etapa 3")
    canvas.drawRightString(A4[0] - 2.4 * cm, 1 * cm, "Página %d" % d.page)
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF gerado em", OUT)
