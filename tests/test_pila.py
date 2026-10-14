import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from estructuras.pila_lifo import PilaLIFO


class TestPila(unittest.TestCase):

    def test_vacia(self):
        pila = PilaLIFO()
        self.assertTrue(pila.is_empty())
        self.assertIsNone(pila.pop())
        self.assertIsNone(pila.peek())

    def test_orden_lifo(self):
        pila = PilaLIFO()
        for x in (1, 2, 3):
            pila.push(x)
        self.assertEqual(pila.peek(), 3)
        self.assertEqual([pila.pop(), pila.pop(), pila.pop()], [3, 2, 1])
        self.assertTrue(pila.is_empty())

    def test_listar_desde_el_tope(self):
        pila = PilaLIFO()
        pila.push("a")
        pila.push("b")
        self.assertEqual(pila.listar(), ["b", "a"])
        self.assertEqual(len(pila), 2)


if __name__ == "__main__":
    unittest.main()
