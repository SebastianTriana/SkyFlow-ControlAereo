class ColaPrioridad:
    """
    Min-Heap para los aterrizajes: sale primero el menor nivel_emergencia (1 = más urgente).
    Se guarda en un arreglo: el padre de i está en (i-1)//2, los hijos en 2i+1 y 2i+2.
    """

    def __init__(self):
        self.datos = []

    def is_empty(self):
        # Complejidad: O(1)
        return len(self.datos) == 0

    def insert(self, vuelo):
        # Complejidad: O(log n)
        # Se pone al final del arreglo y se sube mientras sea más urgente que su padre.
        self.datos.append(vuelo)
        self._subir(len(self.datos) - 1)

    def extract_min(self):
        # Complejidad: O(log n)
        # Se saca la raíz, el último pasa a la raíz y se baja hasta su lugar.
        if self.is_empty():
            return None
        raiz = self.datos[0]
        ultimo = self.datos.pop()
        if not self.is_empty():
            self.datos[0] = ultimo
            self._bajar(0)
        return raiz

    def peek(self):
        # Complejidad: O(1)
        if self.is_empty():
            return None
        return self.datos[0]

    def remove(self, vuelo):
        # Complejidad: O(n) para buscar el vuelo + O(log n) para reacomodar (se usa en undo)
        # El último ocupa el hueco y se sube o baja según corresponda.
        i = self.datos.index(vuelo)
        ultimo = self.datos.pop()
        if i < len(self.datos):
            self.datos[i] = ultimo
            self._subir(i)
            self._bajar(i)

    def __len__(self):
        # Complejidad: O(1)
        return len(self.datos)

    def _subir(self, i):
        # Complejidad: O(log n): intercambia con el padre mientras sea más urgente.
        while i > 0:
            padre = (i - 1) // 2
            if self.datos[i].nivel_emergencia >= self.datos[padre].nivel_emergencia:
                break
            self._intercambiar(i, padre)
            i = padre

    def _bajar(self, i):
        # Complejidad: O(log n): intercambia con el hijo más urgente mientras haga falta.
        while True:
            menor = i
            for hijo in (2 * i + 1, 2 * i + 2):
                if hijo < len(self.datos) and \
                        self.datos[hijo].nivel_emergencia < self.datos[menor].nivel_emergencia:
                    menor = hijo
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor

    def _intercambiar(self, a, b):
        self.datos[a], self.datos[b] = self.datos[b], self.datos[a]
