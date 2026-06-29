import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "prints")
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1380, "height": 920}, device_scale_factor=2)
    page.goto("http://localhost:5173/", wait_until="networkidle")
    page.wait_for_timeout(700)
    page.click(".sidebar button:nth-of-type(3)")  # Efetuar Compra
    page.wait_for_timeout(800)
    page.fill('input[type="number"]', "10000")
    page.select_option('.card select >> nth=0', value="14")  # fornecedor IRREGULAR
    page.select_option('.card select >> nth=1', index=1)      # primeiro orcamento
    page.wait_for_timeout(300)
    page.click("button.btn.green")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT, "07_compra_bloqueada.png"), full_page=True)
    b.close()
print("OK")
