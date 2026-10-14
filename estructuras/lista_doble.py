class NodoDoble:
    """Nodo con dos punteros: al anterior y al siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None


class ListaDoble:
    """
    Lista doblemente enlazada para el radar de vuelos activos.
    Punteros de la lista: 'cabeza' (primer nodo) y 'cola' (último nodo).
    """

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insert(self, dato):
        # Complejidad: O(1)
        # Punteros: nuevo.anterior = cola; cola.siguiente = nuevo; cola avanza al nuevo.
        # Devuelve el nodo para poder borrarlo después en O(1).
        nuevo = NodoDoble(dato)
        if self.cola is None:
            self.cabeza = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
        self.cola = nuevo
        self.tamano += 1
        return nuevo

    def remove(self, nodo):
        # Complejidad: O(1) (ya tenemos el nodo, no hay que buscarlo)
        # Punteros: el anterior salta al siguiente y el siguiente apunta de vuelta al anterior.
        if nodo.anterior is None:
            self.cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente
        if nodo.siguiente is None:
            self.cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior
        nodo.anterior = None
        nodo.siguiente = None
        self.tamano -= 1

    def find(self, codigo):
        # Complejidad: O(n)
        # Punteros: 'actual' recorre desde cabeza hasta encontrar el código del vuelo.
        actual = self.cabeza
        while actual is not None:
            if actual.dato.codigo == codigo:
                return actual
            actual = actual.siguiente
        return None

    def __len__(self):
        # Complejidad: O(1)
        return self.tamano

    def listar(self):
        # Complejidad: O(n)
        # Punteros: 'actual' recorre desde cabeza hasta None sin modificar la lista.
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos
