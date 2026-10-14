class NodoPila:
    """Nodo simple: guarda un dato y apunta al nodo de abajo."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class PilaLIFO:
    """
    Pila LIFO para el historial de comandos de la torre (undo).
    Un solo puntero: 'tope' (el último comando guardado).
    """

    def __init__(self):
        self.tope = None
        self.tamano = 0

    def is_empty(self):
        # Complejidad: O(1)
        return self.tope is None

    def push(self, dato):
        # Complejidad: O(1)
        # Punteros: el nuevo nodo apunta al tope actual y luego tope pasa a ser el nuevo.
        nuevo = NodoPila(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.tamano += 1

    def pop(self):
        # Complejidad: O(1)
        # Punteros: tope baja al nodo siguiente (el de abajo).
        if self.is_empty():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamano -= 1
        return dato

    def peek(self):
        # Complejidad: O(1)
        # Punteros: no se mueve ninguno, solo se lee tope.
        if self.is_empty():
            return None
        return self.tope.dato

    def __len__(self):
        # Complejidad: O(1)
        return self.tamano

    def listar(self):
        # Complejidad: O(n)
        # Punteros: 'actual' recorre desde tope (el más reciente) hasta None.
        datos = []
        actual = self.tope
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos
