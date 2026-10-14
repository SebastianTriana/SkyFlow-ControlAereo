import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modelos.vuelo import Vuelo
from estructuras.cola_fifo import ColaFIFO


class TestColaDespegues(unittest.TestCase):

    def setUp(self):
        self.cola = ColaFIFO()
        self.v1 = Vuelo("AV101", "Avianca", "MDE")
        self.v2 = Vuelo("LA202", "LATAM", "LIM")
        self.v3 = Vuelo("CM303", "Copa", "PTY")

    def test_cola_nueva_esta_vacia(self):
        self.assertTrue(self.cola.is_empty())
        self.assertIsNone(self.cola.dequeue())
        self.assertIsNone(self.cola.peek())

    def test_orden_fifo(self):
        self.cola.enqueue(self.v1)
        self.cola.enqueue(self.v2)
        self.cola.enqueue(self.v3)
        self.assertEqual(self.cola.dequeue(), self.v1)
        self.assertEqual(self.cola.dequeue(), self.v2)
        self.assertEqual(self.cola.dequeue(), self.v3)
        self.assertTrue(self.cola.is_empty())

    def test_peek_no_extrae(self):
        self.cola.enqueue(self.v1)
        self.cola.enqueue(self.v2)
        self.assertEqual(self.cola.peek(), self.v1)
        self.assertEqual(len(self.cola), 2)

    def test_reutilizar_cola_tras_vaciarla(self):
        self.cola.enqueue(self.v1)
        self.cola.dequeue()
        self.assertIsNone(self.cola.final)
        self.cola.enqueue(self.v2)
        self.assertEqual(self.cola.peek(), self.v2)
        self.assertEqual(len(self.cola), 1)

    def test_listar(self):
        self.cola.enqueue(self.v1)
        self.cola.enqueue(self.v2)
        self.assertEqual(self.cola.listar(), [self.v1, self.v2])

    def test_enqueue_front(self):
        self.cola.enqueue_front(self.v1)
        self.assertIs(self.cola.final, self.cola.frente)  # un solo nodo
        self.cola.enqueue_front(self.v2)
        self.assertEqual(self.cola.listar(), [self.v2, self.v1])

    def test_remove_last(self):
        self.assertIsNone(self.cola.remove_last())
        self.cola.enqueue(self.v1)
        self.cola.enqueue(self.v2)
        self.assertEqual(self.cola.remove_last(), self.v2)
        self.assertEqual(self.cola.listar(), [self.v1])
        self.assertEqual(self.cola.remove_last(), self.v1)
        self.assertIsNone(self.cola.frente)
        self.assertIsNone(self.cola.final)


if __name__ == "__main__":
    unittest.main()
