"""Pruebas unitarias para las alertas del laboratorio."""

import unittest
from unittest.mock import patch

import config
import eventos.detectores as detectores
import eventos.manejadores as manejadores


class PruebasAlertas(unittest.TestCase):
    def setUp(self):
        # LABORATORIO: reiniciar estados internos para que cada prueba sea aislada.
        detectores._estado["alarma"].clear()
        detectores._estado["red_desconectada_desde"] = None
        detectores._estado["red_ultimo_recordatorio"] = None

    def lectura_red(self, conectada, evento=None, valor=0.0):
        return {
            "valor": valor,
            "extra": {"conectada": conectada, "evento_conexion": evento},
        }

    def test_red_desconectada(self):
        eventos = detectores._red(self.lectura_red(False, "red_desconectada"))
        self.assertIn("red_desconectada", [nombre for nombre, _ in eventos])

    def test_red_conectada(self):
        detectores._red(self.lectura_red(False, "red_desconectada"))
        eventos = detectores._red(self.lectura_red(True, "red_conectada"))
        self.assertIn("red_conectada", [nombre for nombre, _ in eventos])

    def test_red_sigue_desconectada(self):
        with patch("eventos.detectores.time.monotonic", side_effect=[0.0, config.RED_RECORDATORIO_SEGUNDOS + 1]):
            detectores._red(self.lectura_red(False, "red_desconectada"))
            eventos = detectores._red(self.lectura_red(False))
        self.assertIn("red_sigue_desconectada", [nombre for nombre, _ in eventos])

    def test_red_pico(self):
        eventos = detectores._red(self.lectura_red(True, valor=config.RED_PICO_KBS))
        self.assertIn("red_pico", [nombre for nombre, _ in eventos])

    def test_manejadores_red(self):
        self.assertEqual(manejadores.red_desconectada({})[0], "ALERTA")
        self.assertEqual(manejadores.red_conectada({})[0], "INFO")
        self.assertEqual(manejadores.red_sigue_desconectada({"segundos": 31.0})[0], "ALERTA")


if __name__ == "__main__":
    unittest.main()
