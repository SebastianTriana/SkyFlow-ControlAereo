from modelos.vuelo import Vuelo
from estructuras.cola_fifo import ColaFIFO
from estructuras.lista_doble import ListaDoble
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.pila_lifo import PilaLIFO


class Simulador:
    """
    Torre de control: conecta las 4 estructuras.
      despegues   (ColaFIFO)      -> fila de carreteo y despegue
      radar       (ListaDoble)    -> vuelos activos en el aire
      aterrizajes (ColaPrioridad) -> vuelos que piden aterrizar, el más urgente primero
      historial   (PilaLIFO)      -> comandos ejecutados, para deshacer
    """

    def __init__(self):
        self.despegues = ColaFIFO()
        self.radar = ListaDoble()
        self.aterrizajes = ColaPrioridad()
        self.historial = PilaLIFO()

    def pedir_despegue(self, codigo, aerolinea, destino):
        vuelo = Vuelo(codigo, aerolinea, destino)
        self.despegues.enqueue(vuelo)
        self.historial.push(("PEDIR_DESPEGUE", vuelo))
        return vuelo

    def despegar(self):
        # Sale el primero de la fila y entra al radar.
        vuelo = self.despegues.dequeue()
        if vuelo is None:
            return None
        vuelo.estado = "EN_VUELO"
        vuelo.nodo_radar = self.radar.insert(vuelo)
        self.historial.push(("DESPEGAR", vuelo))
        return vuelo

    def solicitar_aterrizaje(self, codigo, nivel):
        # Solo puede pedir aterrizaje un vuelo que está volando en el radar.
        nodo = self.radar.find(codigo)
        if nodo is None or nodo.dato.estado != "EN_VUELO":
            return None
        vuelo = nodo.dato
        vuelo.nivel_emergencia = nivel
        vuelo.estado = "ESPERANDO_ATERRIZAJE"
        self.aterrizajes.insert(vuelo)
        self.historial.push(("SOLICITAR_ATERRIZAJE", vuelo))
        return vuelo

    def aterrizar(self):
        # Aterriza el más urgente y sale del radar.
        vuelo = self.aterrizajes.extract_min()
        if vuelo is None:
            return None
        self.radar.remove(vuelo.nodo_radar)
        vuelo.nodo_radar = None
        vuelo.estado = "ATERRIZADO"
        self.historial.push(("ATERRIZAR", vuelo))
        return vuelo

    def deshacer(self):
        # Saca el último comando de la pila y hace lo contrario.
        comando = self.historial.pop()
        if comando is None:
            return None
        tipo, vuelo = comando
        if tipo == "PEDIR_DESPEGUE":
            self.despegues.remove_last()
        elif tipo == "DESPEGAR":
            self.radar.remove(vuelo.nodo_radar)
            vuelo.nodo_radar = None
            vuelo.estado = "EN_ESPERA"
            self.despegues.enqueue_front(vuelo)
        elif tipo == "SOLICITAR_ATERRIZAJE":
            self.aterrizajes.remove(vuelo)
            vuelo.estado = "EN_VUELO"
        elif tipo == "ATERRIZAR":
            vuelo.estado = "ESPERANDO_ATERRIZAJE"
            vuelo.nodo_radar = self.radar.insert(vuelo)
            self.aterrizajes.insert(vuelo)
        return comando
