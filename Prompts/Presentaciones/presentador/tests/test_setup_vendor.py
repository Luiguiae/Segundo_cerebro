"""Tests de setup_vendor.py sin red: integridad, tarballs hostiles y aborto ante hash alterado."""
import base64
import hashlib
import io
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import setup_vendor as sv


def tgz(entradas: dict) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for nombre, contenido in entradas.items():
            info = tarfile.TarInfo(nombre)
            info.size = len(contenido)
            t.addfile(info, io.BytesIO(contenido))
    return buf.getvalue()


def integrity(datos: bytes) -> str:
    return "sha512-" + base64.b64encode(hashlib.sha512(datos).digest()).decode()


class Integridad(unittest.TestCase):
    def test_sha512_correcto_pasa(self):
        d = b"hola"
        sv.verificar_sha512_npm(d, integrity(d))

    def test_sha512_alterado_falla(self):
        with self.assertRaises(sv.ErrorIntegridad):
            sv.verificar_sha512_npm(b"hola", integrity(b"otra cosa"))

    def test_sha256_alterado_falla(self):
        with self.assertRaises(sv.ErrorIntegridad):
            sv.verificar_sha256(b"hola", "0" * 64)

    def test_tarball_con_ruta_fuera_es_rechazado(self):
        malo = tgz({"../escape.txt": b"x"})
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(sv.ErrorIntegridad):
                sv._extraer_seguro(malo, Path(tmp) / "dest")
            self.assertFalse((Path(tmp) / "escape.txt").exists())


class Aborto(unittest.TestCase):
    def test_hash_alterado_aborta_y_no_instala(self):
        with tempfile.TemporaryDirectory() as tmp:
            vendor = Path(tmp) / "vendor"
            falso = tgz({"package/dist/reveal.js": b"//"})
            with mock.patch.object(sv, "VENDOR", vendor), \
                 mock.patch.object(sv, "descargar", return_value=falso), \
                 mock.patch.object(sv, "REVEAL_INTEGRITY", integrity(b"otro")):
                self.assertEqual(sv.main(["--forzar"]), 1)
            self.assertFalse((vendor / "reveal").exists())
            self.assertFalse((vendor / sv.MARCA).exists())

    def test_faltantes_lista_lo_que_no_existe(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(sorted(sv.faltantes(Path(tmp))), sorted(sv.ARCHIVOS_REQUERIDOS))


if __name__ == "__main__":
    unittest.main()
