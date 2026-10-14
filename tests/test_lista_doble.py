import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modelos.vuelo import Vuelo
from estructuras.lista_doble import ListaDoble


class TestListaDoble(unittest.TestCase):

    def setUp(self):
        self.lista = ListaDoble()
        self.v1, self.v2, self.v3 = Vuelo("A1", "X", "P"), Vuelo("A2", "X", "P"), Vuelo("A3", "X", "P")
        self.n1 = self.lista.insert(self.v1)
        self.n2 = self.lista.insert(self.v2)
        self.n3 = self.lista.insert(self.v3)

    def test_insert_enlaza_ambos_sentidos(self):
        self.assertEqual(self.lista.listar(), [self.v1, self.v2, self.v3])
        self.assertIs(self.n2.anterior, self.n1)
        self.assertIs(self.n2.siguiente, self.n3)

    def test_remove_medio(self):
        self.lista.remove(self.n2)
        self.assertEqual(self.lista.listar(), [self.v1, self.v3])
        self.assertIs(self.n3.anterior, self.n1)

    def test_remove_extremos(self):
        self.lista.remove(self.n1)
        self.assertIs(self.lista.cabeza, self.n2)
        self.lista.remove(self.n3)
        self.assertIs(self.lista.cola, self.n2)

    def test_remove_hasta_vaciar(self):
        for nodo in (self.n1, self.n2, self.n3):
            self.lista.remove(nodo)
        self.assertIsNone(self.lista.cabeza)
        self.assertIsNone(self.lista.cola)
        self.assertEqual(len(self.lista), 0)

    def test_find(self):
        self.assertIs(self.lista.find("A2"), self.n2)
        self.assertIsNone(self.lista.find("ZZ"))


if __name__ == "__main__":
    unittest.main()
