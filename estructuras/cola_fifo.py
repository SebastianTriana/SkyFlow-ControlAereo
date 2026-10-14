class NodoCola:
    """Nodo simple: guarda un dato y apunta al siguiente nodo."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ColaFIFO:
    """
    Cola FIFO para la fila de carreteo y despegues.
    Usa dos punteros: 'frente' (sale primero) y 'final' (entra último).
    """

    def __init__(self):
        self.frente = None
        self.final = None
        self.tamano = 0

    def is_empty(self):
        # Complejidad: O(1)
        return self.frente is None

    def enqueue(self, dato):
        # Complejidad: O(1)
        # Punteros: final.siguiente apunta al nuevo nodo y luego final avanza a él.
        nuevo = NodoCola(dato)
        if self.is_empty():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.tamano += 1

    def dequeue(self):
        # Complejidad: O(1)
        # Punteros: frente avanza al siguiente nodo; si la cola queda vacía, final = None.
        if self.is_empty():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamano -= 1
        return dato

    def peek(self):
        # Complejidad: O(1)
        # Punteros: no se mueve ninguno, solo se lee frente.
        if self.is_empty():
            return None
        return self.frente.dato

    def __len__(self):
        # Complejidad: O(1)
        return self.tamano

    def listar(self):
        # Complejidad: O(n)
        # Punteros: 'actual' recorre desde frente hasta None sin modificar la cola.
        datos = []
        actual = self.frente
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def enqueue_front(self, dato):
        # Complejidad: O(1)
        # Punteros: el nuevo nodo apunta al frente actual y frente pasa a ser el nuevo.
        # Se usa en undo para devolver un avión al inicio de la fila.
        nuevo = NodoCola(dato)
        nuevo.siguiente = self.frente
        self.frente = nuevo
        if self.final is None:
            self.final = nuevo
        self.tamano += 1

    def remove_last(self):
        # Complejidad: O(n) (hay que recorrer hasta el penúltimo nodo)
        # Punteros: 'actual' llega al penúltimo; final retrocede a él y su siguiente = None.
        # Se usa en undo para anular el último avión encolado.
        if self.is_empty():
            return None
        dato = self.final.dato
        if self.frente is self.final:
            self.frente = None
            self.final = None
        else:
            actual = self.frente
            while actual.siguiente is not self.final:
                actual = actual.siguiente
            actual.siguiente = None
            self.final = actual
        self.tamano -= 1
        return dato
