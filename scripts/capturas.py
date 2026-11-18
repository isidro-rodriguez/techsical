"""Capturas de la web de demostración para revisar el tema a ojo.

Sirve ``site/`` (constrúyelo antes con ``uv run zensical build``) y guarda en
``capturas/`` una imagen por página, esquema (claro y oscuro) y tamaño (escritorio
y móvil). Necesita Playwright y Chrome, Edge o ``playwright install chromium``::

    uv run --with playwright python scripts/capturas.py [--full]
"""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "inicio": "",
    "instalacion": "guia/instalacion/",
    "paginas": "guia/paginas/",
    "muestrario": "muestrario/",
}
SIZES = {"escritorio": (1440, 900), "movil": (390, 844)}
SCHEMES = ("light", "dark")


class _Quiet(http.server.SimpleHTTPRequestHandler):
    """Servidor estático sin registro de peticiones."""

    def log_message(self, format: str, *args: object) -> None:
        """No escribe nada por petición."""


def _serve(site: Path) -> tuple[http.server.ThreadingHTTPServer, str]:
    """Sirve ``site`` en un puerto libre y devuelve el servidor y su URL."""
    handler = functools.partial(_Quiet, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}/"


def main() -> int:
    """Genera las capturas; devuelve el código de salida."""
    from playwright.sync_api import sync_playwright

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="página completa")
    parser.add_argument("--out", type=Path, default=ROOT / "capturas")
    args = parser.parse_args()
    site = ROOT / "site"
    if not (site / "index.html").exists():
        print("Falta site/: ejecuta antes `uv run zensical build`.", file=sys.stderr)
        return 1
    args.out.mkdir(exist_ok=True)
    server, base = _serve(site)
    try:
        with sync_playwright() as pw:
            browser = None
            for channel in ("chrome", "msedge", None):
                try:
                    browser = pw.chromium.launch(channel=channel)
                    break
                except Exception:
                    continue
            if browser is None:
                print("No hay navegador para Playwright.", file=sys.stderr)
                return 1
            for scheme in SCHEMES:
                for size, (width, height) in SIZES.items():
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        color_scheme=scheme,
                        device_scale_factor=1,
                    )
                    page = context.new_page()
                    for name, rel in PAGES.items():
                        page.goto(base + rel, wait_until="networkidle")
                        page.evaluate("document.fonts.ready")
                        path = args.out / f"{name}-{scheme}-{size}.png"
                        page.screenshot(path=str(path), full_page=args.full)
                        print(path.relative_to(ROOT))
                    context.close()
            browser.close()
    finally:
        server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
