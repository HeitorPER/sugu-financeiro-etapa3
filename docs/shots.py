"""Captura prints de cada tela da aplicacao usando Playwright."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "prints")
os.makedirs(OUT, exist_ok=True)
URL = "http://localhost:5173/"

# indice do botao no menu lateral (1-based) -> nome do arquivo
NAV = {
    1: "01_dashboard",
    2: "02_fornecedores",
    3: "03_compras",
    4: "04_licitacoes",
    5: "05_pagamentos",
    6: "06_relatorios",
}


def shot(page, name):
    page.screenshot(path=os.path.join(OUT, name + ".png"), full_page=True)
    print("ok", name)


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1380, "height": 920}, device_scale_factor=2)
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(800)

    for idx, name in NAV.items():
        page.click(f".sidebar button:nth-of-type({idx})")
        page.wait_for_timeout(900)
        if name == "04_licitacoes":
            # abre a primeira licitacao para exibir as propostas
            page.click(".card table .btn.ghost.sm")
            page.wait_for_timeout(700)
        shot(page, name)

    # ---- Tela extra: compra bloqueada por regra de negocio (trigger) ----
    page.click(".sidebar button:nth-of-type(3)")  # Efetuar Compra
    page.wait_for_timeout(700)
    page.fill('input[type="number"]', "10000")
    # fornecedor IRREGULAR (Materiais Diversos SA / Servicos Gerais ME) e um orcamento
    page.select_option('select >> nth=0',
                       label=[o for o in page.locator('select >> nth=0 option').all_inner_texts()
                              if "IRREGULAR" in o][0])
    page.select_option('select >> nth=1', index=1)
    page.click("button.btn.green")
    page.wait_for_timeout(900)
    shot(page, "07_compra_bloqueada")

    b.close()
print("DONE")
