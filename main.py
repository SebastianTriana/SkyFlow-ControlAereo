from simulador import Simulador

MENU = """
===== SKYFLOW - TORRE DE CONTROL =====
1. Pedir despegue (nuevo vuelo a la fila)
2. Despegar siguiente
3. Solicitar aterrizaje / declarar emergencia
4. Aterrizar el más urgente
5. Ver fila de despegue
6. Ver radar
7. Ver cola de aterrizaje
8. Deshacer último comando
9. Ver historial
G. Abrir Interfaz Gráfica (Tkinter)
0. Salir"""


def mostrar(titulo, vuelos):
    print(f"--- {titulo} ({len(vuelos)}) ---")
    for vuelo in vuelos:
        print(vuelo)


def opcion_pedir(torre):
    codigo = input("Código: ")
    aerolinea = input("Aerolínea: ")
    destino = input("Destino: ")
    print("En fila:", torre.pedir_despegue(codigo, aerolinea, destino))


def opcion_solicitar(torre):
    codigo = input("Código del vuelo en el radar: ")
    nivel = input("Nivel de emergencia (1 = crítico ... 4 = normal): ")
    if nivel not in ("1", "2", "3", "4"):
        print("Nivel inválido.")
        return
    vuelo = torre.solicitar_aterrizaje(codigo, int(nivel))
    print("Solicitud registrada:" if vuelo else "Ese vuelo no está volando.", vuelo or "")


def mostrar_resultado(texto, vuelo):
    print(f"{texto}: {vuelo}" if vuelo else "No hay vuelos disponibles.")


def main():
    torre = Simulador()
    while True:
        print(MENU)
        op = input("Opción: ")
        if op == "1":
            opcion_pedir(torre)
        elif op == "2":
            mostrar_resultado("Despegó", torre.despegar())
        elif op == "3":
            opcion_solicitar(torre)
        elif op == "4":
            mostrar_resultado("Aterrizó", torre.aterrizar())
        elif op == "5":
            mostrar("Fila de despegue", torre.despegues.listar())
        elif op == "6":
            mostrar("Radar", torre.radar.listar())
        elif op == "7":
            mostrar("Cola de aterrizaje (orden interno del heap)", torre.aterrizajes.datos)
        elif op == "8":
            comando = torre.deshacer()
            print(f"Deshecho: {comando[0]} {comando[1].codigo}" if comando else "Nada que deshacer.")
        elif op == "9":
            for tipo, vuelo in torre.historial.listar():
                print(f"{tipo} -> {vuelo.codigo}")
        elif op.lower() == "g":
            import gui
            print("Abriendo interfaz gráfica...")
            gui.main()
        elif op == "0":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
