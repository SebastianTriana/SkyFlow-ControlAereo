import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from simulador import Simulador


def torre_con_vuelos_en_el_aire():
    torre = Simulador()
    for codigo in ("A1", "A2", "A3"):
        torre.pedir_despegue(codigo, "X", "P")
    for _ in range(3):
        torre.despegar()
    return torre


class TestSimulador(unittest.TestCase):

    def test_despegue_en_orden_de_llegada(self):
        torre = torre_con_vuelos_en_el_aire()
        self.assertEqual([v.codigo for v in torre.radar.listar()], ["A1", "A2", "A3"])
        self.assertTrue(torre.despegues.is_empty())

    def test_aterriza_primero_el_mas_urgente(self):
        torre = torre_con_vuelos_en_el_aire()
        torre.solicitar_aterrizaje("A1", 3)
        torre.solicitar_aterrizaje("A2", 1)
        self.assertEqual(torre.aterrizar().codigo, "A2")
        self.assertEqual(torre.aterrizar().codigo, "A1")
        self.assertEqual([v.codigo for v in torre.radar.listar()], ["A3"])

    def test_no_pide_aterrizaje_quien_no_esta_en_el_radar(self):
        torre = Simulador()
        torre.pedir_despegue("A1", "X", "P")
        self.assertIsNone(torre.solicitar_aterrizaje("A1", 1))
        self.assertIsNone(torre.solicitar_aterrizaje("ZZ", 1))

    def test_deshacer_pedir_despegue(self):
        torre = Simulador()
        torre.pedir_despegue("A1", "X", "P")
        torre.pedir_despegue("A2", "X", "P")
        torre.deshacer()
        self.assertEqual([v.codigo for v in torre.despegues.listar()], ["A1"])

    def test_deshacer_despegar_devuelve_al_frente(self):
        torre = Simulador()
        torre.pedir_despegue("A1", "X", "P")
        torre.pedir_despegue("A2", "X", "P")
        torre.despegar()
        torre.deshacer()
        self.assertEqual([v.codigo for v in torre.despegues.listar()], ["A1", "A2"])
        self.assertEqual(len(torre.radar), 0)

    def test_deshacer_solicitud_y_aterrizaje(self):
        torre = torre_con_vuelos_en_el_aire()
        torre.solicitar_aterrizaje("A2", 1)
        torre.aterrizar()
        torre.deshacer()  # deshace aterrizar
        self.assertEqual(len(torre.radar), 3)
        self.assertEqual(torre.aterrizajes.peek().codigo, "A2")
        torre.deshacer()  # deshace solicitar
        self.assertTrue(torre.aterrizajes.is_empty())
        self.assertEqual(torre.radar.find("A2").dato.estado, "EN_VUELO")

    def test_deshacer_sin_historial(self):
        self.assertIsNone(Simulador().deshacer())


if __name__ == "__main__":
    unittest.main()
