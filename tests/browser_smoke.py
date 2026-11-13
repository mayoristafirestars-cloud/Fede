"""Optional browser checks. Run with Python that has Playwright and Pillow.

APP_PYTHON selects the interpreter with requirements.txt installed.
CHROMIUM_PATH defaults to the managed environment's system Chromium.
All application data lives in an automatically removed temporary directory.
"""
import io
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from playwright.sync_api import expect, sync_playwright

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="verduleria-browser-") as tmp:
    env = {**os.environ, "CORONEL_DB_PATH": tmp + "/browser.db", "CORONEL_MEDIA_DIR": tmp + "/photos"}
    with open(tmp + "/server.log", "w+") as log:
        process = subprocess.Popen([
            os.environ.get("APP_PYTHON", sys.executable), "-m", "uvicorn", "main:app",
            "--app-dir", "backend", "--host", "127.0.0.1", "--port", "8002",
        ], cwd=root, env=env, stdout=log, stderr=log)
        try:
            for _ in range(60):
                try:
                    with urllib.request.urlopen("http://127.0.0.1:8002/api/estado", timeout=1):
                        break
                except Exception:
                    if process.poll() is not None:
                        log.seek(0)
                        raise RuntimeError(log.read())
                    time.sleep(.1)
            else:
                raise RuntimeError("Test server did not start")
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"), headless=True, args=["--no-sandbox"])
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page.set_default_timeout(10000)
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto("http://127.0.0.1:8002")
                expect(page.get_by_text("0 de 6 puntos relevados")).to_be_visible()
                page.get_by_label("Nombre del negocio", exact=True).fill("Verdulería de prueba")
                page.get_by_label("Localidad", exact=True).fill("Córdoba")
                for name, value in [("atencion", "mostrador"), ("pesaje", "en_caja"), ("cobro", "misma_persona"), ("entrega", "en_local")]:
                    page.locator(f"[name={name}]").select_option(value)
                page.get_by_role("button", name="+ Agregar persona").click()
                page.locator("[data-field=nombre]").fill("Ana")
                page.locator("[data-field=rol]").select_option("dueno")
                page.get_by_role("button", name="+ Agregar equipo").click()
                page.locator("[data-field=marca_modelo]").fill("Modelo pendiente de prueba")
                page.get_by_label("Efectivo", exact=True).check()
                page.locator("#save-business").click()
                expect(page.get_by_text("3 de 6 puntos relevados")).to_be_visible()
                expect(page.locator("#save-state")).to_have_text("Sin cambios pendientes")
                page.reload()
                expect(page.get_by_label("Nombre del negocio", exact=True)).to_have_value("Verdulería de prueba")
                expect(page.locator("[data-field=nombre]")).to_have_value("Ana")
                expect(page.locator("#save-state")).to_have_text("Sin cambios pendientes")
                page.get_by_role("link", name="Productos").click()
                page.get_by_role("button", name="+ Crear primer producto").click()
                page.locator('#product-form [name=descripcion]').fill("Tomate")
                page.locator('#product-form [name=codigo]').fill("TOM-01")
                page.get_by_label("Variedad", exact=True).fill("Perita")
                page.get_by_label("Calidad", exact=True).fill("Primera")
                page.get_by_label("Presentación", exact=True).fill("Suelto")
                page.locator('#product-form [name=aliases]').fill("jitomate, tomatito")
                image = io.BytesIO()
                Image.new("RGB", (100, 100), (210, 70, 45)).save(image, "PNG")
                page.locator('#product-form [name=foto]').set_input_files({"name": "tomate.png", "mimeType": "image/png", "buffer": image.getvalue()})
                page.get_by_role("button", name="Guardar producto", exact=True).click()
                expect(page.locator("#product-dialog")).not_to_be_visible()
                expect(page.get_by_role("heading", name="Tomate", exact=True)).to_be_visible()
                expect(page.locator(".product-photo img")).to_have_js_property("naturalWidth", 100)
                assert page.locator('.product-photo img').evaluate('(el) => el.getBoundingClientRect().bottom <= el.parentElement.getBoundingClientRect().bottom + 1'), 'Photo overlaps product details'
                page.get_by_role("button", name="Editar producto").click()
                page.get_by_label("Unidad de venta", exact=True).select_option("unidad")
                page.get_by_role("button", name="Guardar producto", exact=True).click()
                expect(page.locator(".unit-tag")).to_have_text("Unidad")
                page.get_by_role("button", name="+ Nuevo producto").click()
                page.locator('#product-form [name=descripcion]').fill("Duplicado")
                page.locator('#product-form [name=codigo]').fill("tom-01")
                page.get_by_role("button", name="Guardar producto", exact=True).click()
                expect(page.locator("#product-error")).to_contain_text("ya pertenece")
                page.get_by_role("button", name="Cancelar", exact=True).click()
                page.get_by_role("searchbox", name="Buscar productos").fill("inexistente")
                expect(page.locator(".product-card")).to_have_count(0)
                page.get_by_role("searchbox", name="Buscar productos").fill("JITÓMATE")
                expect(page.locator(".product-card")).to_have_count(1)
                page.reload()
                expect(page.locator(".product-card")).to_have_count(1)
                page.screenshot(path="/tmp/verduleria-productos.png", full_page=True)
                page.set_viewport_size({"width": 390, "height": 844})
                expect(page.get_by_role("button", name="+ Nuevo producto")).to_be_visible()
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile horizontal overflow"
                page.get_by_role("button", name="+ Nuevo producto").click()
                expect(page.locator('#product-form [name=descripcion]')).to_be_visible()
                page.get_by_role("button", name="Cancelar", exact=True).click()
                page.screenshot(path="/tmp/verduleria-movil.png", full_page=True)
                assert not errors, errors
                browser.close()
                print("PASS: settings save/reload, staff/equipment, product create/photo/edit, duplicate rejection, alias search, reload and mobile; no JS errors.")
        finally:
            process.terminate()
            process.wait(timeout=10)
