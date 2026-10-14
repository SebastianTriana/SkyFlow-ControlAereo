class Vuelo:
    """Representa una aeronave dentro del espacio aéreo o la pista."""

    def __init__(self, codigo, aerolinea, destino, nivel_emergencia=4, combustible=100):
        self.codigo = codigo
        self.aerolinea = aerolinea
        self.destino = destino
        self.nivel_emergencia = nivel_emergencia  # 1 = más urgente, 4 = normal
        self.combustible = combustible            # minutos de vuelo restantes
        self.estado = "EN_ESPERA"
        self.nodo_radar = None                    # nodo en la lista del radar (para borrar en O(1))

    def __str__(self):
        return (f"[{self.codigo} | {self.aerolinea} -> {self.destino} | "
                f"Prioridad: {self.nivel_emergencia} | Estado: {self.estado}]")
