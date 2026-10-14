import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modelos.vuelo import Vuelo
from estructuras.cola_prioridad import ColaPrioridad


def vuelos(*niveles):
    return [Vuelo(f"V{i}", "X", "P", nivel) for i, nivel in enumerate(niveles)]


class TestColaPrioridad(unittest.TestCase):

    def test_vacia(self):
        heap = ColaPrioridad()
        self.assertIsNone(heap.extract_min())
        self.assertIsNone(heap.peek())

    def test_sale_el_mas_urgente_primero(self):
        heap = ColaPrioridad()
        for v in vuelos(4, 2, 3, 1, 4, 2, 1):
            heap.insert(v)
        salida = []
        while not heap.is_empty():
            salida.append(heap.extract_min().nivel_emergencia)
        self.assertEqual(salida, [1, 1, 2, 2, 3, 4, 4])

    def test_remove_mantiene_el_orden(self):
        heap = ColaPrioridad()
        lista = vuelos(3, 1, 4, 2, 5)
        for v in lista:
            heap.insert(v)
        heap.remove(lista[1])  # quita el de nivel 1
        salida = []
        while not heap.is_empty():
            salida.append(heap.extract_min().nivel_emergencia)
        self.assertEqual(salida, [2, 3, 4, 5])

    def test_remove_el_unico(self):
        heap = ColaPrioridad()
        v = vuelos(1)[0]
        heap.insert(v)
        heap.remove(v)
        self.assertTrue(heap.is_empty())


if __name__ == "__main__":
    unittest.main()
