"""Tests de presentar.py: rutas, seguridad, MIME, vendor incompleto y puerto ocupado."""
import contextlib
import http.client
import io
import socket
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import presentar
import setup_vendor

HTML = "<!doctype html><html><head><meta charset=utf-8></head><body><h1>Hola ñandú</h1></body></html>"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.deck = t / "deck"; (self.deck / "assets").mkdir(parents=True)
        (self.deck / "index.html").write_text(HTML, encoding="utf-8")
        (self.deck / "assets" / "a.js").write_text("console.log(1)", encoding="utf-8")
        (self.deck / ".secret").write_text("no", encoding="utf-8")
        (self.deck / "sin_index").mkdir()
        self.fuera = t / "fuera.txt"; self.fuera.write_text("fuera del deck", encoding="utf-8")
        (self.deck / "escape.txt").symlink_to(self.fuera)
        self.vendor = t / "vendor"
        for rel in setup_vendor.ARCHIVOS_REQUERIDOS:
            f = self.vendor / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(b"x")
        self.proy = t / "proy"; self.proy.mkdir()
        for n in ("presentador.js", "comandos.js", "swipe.js", "presentar.py", "secreto.md"):
            (self.proy / n).write_text(f"// {n}", encoding="utf-8")
        self.srv = presentar.crear_servidor(self.deck, 0, vendor=self.vendor, proyecto=self.proy, inyectar=False)
        self.puerto = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def tearDown(self):
        self.srv.shutdown(); self.srv.server_close(); self.tmp.cleanup()

    def pedir(self, ruta, metodo="GET"):
        c = http.client.HTTPConnection("127.0.0.1", self.puerto, timeout=5)
        c.request(metodo, ruta)  # http.client NO normaliza '..': llega crudo al servidor
        r = c.getresponse(); cuerpo = r.read(); c.close()
        return r, cuerpo


class Rutas(Base):
    def test_raiz_sirve_index(self):
        r, cuerpo = self.pedir("/")
        self.assertEqual(r.status, 200)
        self.assertEqual(cuerpo.decode("utf-8"), HTML)

    def test_index_explicito_y_assets(self):
        self.assertEqual(self.pedir("/index.html")[0].status, 200)
        r, cuerpo = self.pedir("/assets/a.js")
        self.assertEqual((r.status, cuerpo), (200, b"console.log(1)"))

    def test_mime(self):
        self.assertEqual(self.pedir("/vendor/tasks-vision/wasm/vision_wasm_internal.wasm")[0].getheader("Content-Type"), "application/wasm")
        self.assertEqual(self.pedir("/vendor/models/gesture_recognizer.task")[0].getheader("Content-Type"), "application/octet-stream")
        self.assertTrue(self.pedir("/vendor/tasks-vision/vision_bundle.mjs")[0].getheader("Content-Type").startswith("text/javascript"))
        self.assertTrue(self.pedir("/assets/a.js")[0].getheader("Content-Type").startswith("text/javascript"))
        self.assertEqual(self.pedir("/")[0].getheader("Content-Type"), "text/html")

    def test_no_store_y_content_length(self):
        r, cuerpo = self.pedir("/")
        self.assertEqual(r.getheader("Cache-Control"), "no-store")
        self.assertEqual(int(r.getheader("Content-Length")), len(cuerpo))

    def test_head_sin_cuerpo_pero_con_length(self):
        r, cuerpo = self.pedir("/", "HEAD")
        self.assertEqual((r.status, cuerpo), (200, b""))
        self.assertEqual(int(r.getheader("Content-Length")), len(HTML.encode("utf-8")))

    def test_presentador_solo_lista_blanca(self):
        self.assertEqual(self.pedir("/presentador/comandos.js")[0].status, 200)
        self.assertEqual(self.pedir("/presentador/swipe.js")[0].status, 200)
        for prohibido in ("presentar.py", "secreto.md", "setup_vendor.py"):
            self.assertEqual(self.pedir(f"/presentador/{prohibido}")[0].status, 404, prohibido)


class Seguridad(Base):
    def test_traversal_da_404(self):
        for ruta in ("/../presentar.py", "/%2e%2e/presentar.py", "/..%2fpresentar.py", "/assets/../../fuera.txt",
                     "/vendor/../presentar.py", "/vendor/%2e%2e/fuera.txt", "/presentador/../presentar.py",
                     "//etc/passwd", "/%00", "/assets/%2e%2e/%2e%2e/fuera.txt"):
            self.assertEqual(self.pedir(ruta)[0].status, 404, ruta)

    def test_dotfiles_ocultos(self):
        self.assertEqual(self.pedir("/.secret")[0].status, 404)
        self.assertEqual(self.pedir("/vendor/.setup-ok")[0].status, 404)

    def test_symlink_que_escapa_da_404(self):
        self.assertEqual(self.pedir("/escape.txt")[0].status, 404)

    def test_carpeta_sin_index_no_lista(self):
        self.assertEqual(self.pedir("/sin_index/")[0].status, 404)
        self.assertEqual(self.pedir("/assets/")[0].status, 404)

    def test_solo_loopback(self):
        self.assertEqual(self.srv.server_address[0], "127.0.0.1")


class Cli(unittest.TestCase):
    def ejecutar(self, argv, vendor):
        err = io.StringIO()
        with mock.patch.object(presentar, "VENDOR", vendor), contextlib.redirect_stderr(err):
            codigo = presentar.main(argv)
        return codigo, err.getvalue()

    def deck(self, t):
        d = Path(t) / "deck"; d.mkdir(); (d / "index.html").write_text(HTML, encoding="utf-8"); return d

    def test_vendor_ausente_se_detiene_y_apunta_a_setup(self):
        with tempfile.TemporaryDirectory() as t:
            codigo, err = self.ejecutar([str(self.deck(t)), "--no-abrir"], Path(t) / "no_existe")
        self.assertEqual(codigo, 2)
        self.assertIn("setup_vendor.py", err)

    def test_vendor_incompleto_se_detiene(self):
        with tempfile.TemporaryDirectory() as t:
            v = Path(t) / "vendor"; (v / "reveal/dist").mkdir(parents=True); (v / "reveal/dist/reveal.js").write_bytes(b"x")
            codigo, err = self.ejecutar([str(self.deck(t)), "--no-abrir"], v)
        self.assertEqual(codigo, 2)
        self.assertIn("incompleto", err)
        self.assertIn("setup_vendor.py", err)

    def test_carpeta_inexistente_y_sin_index(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(self.ejecutar([str(Path(t) / "nada")], Path(t))[0], 1)
            vacia = Path(t) / "vacia"; vacia.mkdir()
            codigo, err = self.ejecutar([str(vacia)], Path(t))
            self.assertEqual(codigo, 1); self.assertIn("index.html", err)

    def test_puerto_ocupado_da_mensaje_claro(self):
        with tempfile.TemporaryDirectory() as t, socket.socket() as s:
            v = Path(t) / "vendor"
            for rel in setup_vendor.ARCHIVOS_REQUERIDOS:
                f = v / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(b"x")
            s.bind(("127.0.0.1", 0)); s.listen(1)
            codigo, err = self.ejecutar([str(self.deck(t)), "--no-abrir", "--port", str(s.getsockname()[1])], v)
        self.assertEqual(codigo, 1)
        self.assertIn("ocupado", err)


if __name__ == "__main__":
    unittest.main()
