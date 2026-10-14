import random
import tkinter as tk
from tkinter import messagebox, ttk

from simulador import Simulador

# --- PALETA DE COLORES MODO CLARO ---
COLOR_BG = "#f8fafc"          # Fondo general (blanco pizarra)
COLOR_PANEL = "#ffffff"       # Fondo de tarjetas y paneles
COLOR_BORDE = "#cbd5e1"       # Bordes sutiles
COLOR_TEXTO = "#0f172a"       # Texto principal oscuro
COLOR_SUBTEXTO = "#64748b"    # Texto secundario / gris
COLOR_PISTA = "#334155"       # Asfalto de la pista
COLOR_LINEA_PISTA = "#f8fafc" # Líneas blancas de la pista
COLOR_CIELO = "#f0f9ff"       # Fondo del radar (cielo suave)

# Semáforo de prioridades
COLORES_PRIORIDAD = {
    1: {"bg": "#dc2626", "fg": "#ffffff", "texto": "N1 - Crítico (Mayday)"},
    2: {"bg": "#ea580c", "fg": "#ffffff", "texto": "N2 - Combustible"},
    3: {"bg": "#d97706", "fg": "#ffffff", "texto": "N3 - Falla Técnica"},
    4: {"bg": "#16a34a", "fg": "#ffffff", "texto": "N4 - Normal"},
}

# Aerolíneas y destinos para el generador rápido de demostración
AEROLINEAS_DEMO = [
    ("AV", "Avianca", "MDE"),
    ("LA", "LATAM", "LIM"),
    ("AA", "American", "MIA"),
    ("IB", "Iberia", "MAD"),
    ("CM", "Copa", "PTY"),
    ("AF", "Air France", "CDG"),
]


class InterfazSkyFlow:
    """
    Interfaz gráfica en Tkinter (Modo Claro) para SkyFlow.
    Diseñada pedagógicamente para sustentar las 4 estructuras de datos.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("SkyFlow - Control de Tráfico Aéreo (Modo Claro)")
        self.root.geometry("1180x740")
        self.root.minsize(980, 640)
        self.root.configure(bg=COLOR_BG)

        # Iniciar maximizado automáticamente
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # Atajos para alternar pantalla completa (F11) y salir (Escape)
        self._es_fullscreen = False
        self.root.bind("<F11>", self.alternar_pantalla_completa)
        self.root.bind("<Escape>", self.salir_pantalla_completa)

        # Controlador del backend (sin alterar la lógica de estructuras)
        self.torre = Simulador()
        self.contador_demo = 100

        # Construcción visual
        self._crear_encabezado()
        self._crear_layout_principal()
        self.root.update_idletasks()
        self.actualizar_vistas()
        self.root.after(80, self.actualizar_vistas)

    def alternar_pantalla_completa(self, event=None):
        """Alterna entre modo maximizado y pantalla completa total (F11)."""
        self._es_fullscreen = not self._es_fullscreen
        self.root.attributes("-fullscreen", self._es_fullscreen)
        self.actualizar_vistas()

    def salir_pantalla_completa(self, event=None):
        """Sale de la pantalla completa total al presionar Escape."""
        if self._es_fullscreen:
            self._es_fullscreen = False
            self.root.attributes("-fullscreen", False)
            self.actualizar_vistas()

    # -------------------------------------------------------------
    # CONSTRUCCIÓN DE LA INTERFAZ
    # -------------------------------------------------------------

    def _crear_encabezado(self):
        """Barra superior con título e indicador del proyecto."""
        header = tk.Frame(self.root, bg=COLOR_PANEL, height=60, bd=1, relief="solid")
        header.pack(fill="x", side="top", padx=0, pady=0)

        titulo_box = tk.Frame(header, bg=COLOR_PANEL)
        titulo_box.pack(side="left", padx=20, pady=10)

        lbl_titulo = tk.Label(
            titulo_box,
            text="✈ SKYFLOW",
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_PANEL,
            fg="#0284c7",
        )
        lbl_titulo.pack(side="left")

        lbl_sub = tk.Label(
            titulo_box,
            text=" |  Torre de Control & Visualizador de Estructuras de Datos",
            font=("Segoe UI", 11),
            bg=COLOR_PANEL,
            fg=COLOR_SUBTEXTO,
        )
        lbl_sub.pack(side="left", padx=5)

        # Botón para inyectar vuelos rápidamente en la sustentación
        btn_demo = tk.Button(
            header,
            text="⚡ Cargar Vuelo Demo",
            font=("Segoe UI", 9, "bold"),
            bg="#e0f2fe",
            fg="#0369a1",
            activebackground="#bae6fd",
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.cargar_vuelo_demo,
        )
        btn_demo.pack(side="right", padx=20, pady=12)

    def _crear_layout_principal(self):
        """Divide la pantalla en panel de control (izq) y visualizador gráfico (der)."""
        contenedor = tk.Frame(self.root, bg=COLOR_BG)
        contenedor.pack(fill="both", expand=True, padx=15, pady=12)

        # Panel izquierdo: controles y comandos
        self.panel_izq = tk.Frame(contenedor, bg=COLOR_PANEL, width=320, bd=1, relief="solid")
        self.panel_izq.pack(side="left", fill="y", padx=(0, 12), pady=0)
        self.panel_izq.pack_propagate(False)
        self._construir_panel_izquierdo()

        # Panel derecho: áreas gráficas de las 4 estructuras
        self.panel_der = tk.Frame(contenedor, bg=COLOR_BG)
        self.panel_der.pack(side="right", fill="both", expand=True)
        self._construir_panel_derecho()

    def _construir_panel_izquierdo(self):
        """Controles de la torre: registrar, despegar, emergencias y deshacer."""
        pad_x = 16

        # --- SECCIÓN 1: NUEVO VUELO ---
        lbl_sec1 = tk.Label(
            self.panel_izq,
            text="1. REGISTRAR EN PISTA [Cola FIFO]",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        )
        lbl_sec1.pack(anchor="w", padx=pad_x, pady=(14, 4))

        f_form = tk.Frame(self.panel_izq, bg=COLOR_PANEL)
        f_form.pack(fill="x", padx=pad_x, pady=4)

        tk.Label(f_form, text="Código:", font=("Segoe UI", 9), bg=COLOR_PANEL).grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.txt_codigo = tk.Entry(f_form, font=("Segoe UI", 9), width=10, relief="solid", bd=1)
        self.txt_codigo.grid(row=0, column=1, sticky="w", pady=2, padx=4)
        self.txt_codigo.insert(0, "AV101")

        tk.Label(f_form, text="Aerolínea:", font=("Segoe UI", 9), bg=COLOR_PANEL).grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.txt_aerolinea = tk.Entry(f_form, font=("Segoe UI", 9), width=14, relief="solid", bd=1)
        self.txt_aerolinea.grid(row=1, column=1, sticky="w", pady=2, padx=4)
        self.txt_aerolinea.insert(0, "Avianca")

        tk.Label(f_form, text="Destino:", font=("Segoe UI", 9), bg=COLOR_PANEL).grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.txt_destino = tk.Entry(f_form, font=("Segoe UI", 9), width=10, relief="solid", bd=1)
        self.txt_destino.grid(row=2, column=1, sticky="w", pady=2, padx=4)
        self.txt_destino.insert(0, "MDE")

        btn_encolar = tk.Button(
            self.panel_izq,
            text="+ Encolar para Despegue (O(1))",
            font=("Segoe UI", 9, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
            relief="groove",
            cursor="hand2",
            command=self.accion_pedir_despegue,
        )
        btn_encolar.pack(fill="x", padx=pad_x, pady=(4, 12))

        # --- SECCIÓN 2: OPERACIÓN DE DESPEGUE ---
        lbl_sec2 = tk.Label(
            self.panel_izq,
            text="2. AUTORIZAR DESPEGUE",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        )
        lbl_sec2.pack(anchor="w", padx=pad_x, pady=(6, 2))

        btn_despegar = tk.Button(
            self.panel_izq,
            text="🛫 Despegar Siguiente (FIFO ➔ Radar)",
            font=("Segoe UI", 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.accion_despegar,
        )
        btn_despegar.pack(fill="x", padx=pad_x, pady=(2, 12))

        # --- SECCIÓN 3: DECLARAR EMERGENCIA / SOLICITAR ATERRIZAJE ---
        lbl_sec3 = tk.Label(
            self.panel_izq,
            text="3. SOLICITAR ATERRIZAJE / EMERGENCIA",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        )
        lbl_sec3.pack(anchor="w", padx=pad_x, pady=(6, 4))

        f_emerg = tk.Frame(self.panel_izq, bg=COLOR_PANEL)
        f_emerg.pack(fill="x", padx=pad_x, pady=2)

        tk.Label(f_emerg, text="Vuelo en Radar:", font=("Segoe UI", 9), bg=COLOR_PANEL).grid(
            row=0, column=0, sticky="w"
        )
        self.combo_radar = ttk.Combobox(f_emerg, width=12, state="readonly")
        self.combo_radar.grid(row=0, column=1, sticky="w", padx=4, pady=2)

        tk.Label(f_emerg, text="Prioridad:", font=("Segoe UI", 9), bg=COLOR_PANEL).grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.combo_nivel = ttk.Combobox(
            f_emerg,
            values=[
                "1 - Crítico (Mayday)",
                "2 - Combustible Bajo",
                "3 - Falla Técnica",
                "4 - Normal",
            ],
            width=18,
            state="readonly",
        )
        self.combo_nivel.current(0)
        self.combo_nivel.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        btn_solicitar = tk.Button(
            self.panel_izq,
            text="🚨 Insertar en Cola de Aterrizaje (Min-Heap)",
            font=("Segoe UI", 9, "bold"),
            bg="#fef3c7",
            fg="#92400e",
            relief="groove",
            cursor="hand2",
            command=self.accion_solicitar_aterrizaje,
        )
        btn_solicitar.pack(fill="x", padx=pad_x, pady=(4, 12))

        # --- SECCIÓN 4: ATERRIZAJE PRIORITARIO ---
        lbl_sec4 = tk.Label(
            self.panel_izq,
            text="4. PISTA DE ATERRIZAJE",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        )
        lbl_sec4.pack(anchor="w", padx=pad_x, pady=(6, 2))

        btn_aterrizar = tk.Button(
            self.panel_izq,
            text="🛬 Aterrizar Más Urgente (O(log n))",
            font=("Segoe UI", 9, "bold"),
            bg="#16a34a",
            fg="#ffffff",
            activebackground="#15803d",
            relief="flat",
            cursor="hand2",
            pady=6,
            command=self.accion_aterrizar,
        )
        btn_aterrizar.pack(fill="x", padx=pad_x, pady=(2, 14))

        # Separador visual
        tk.Frame(self.panel_izq, bg=COLOR_BORDE, height=1).pack(fill="x", padx=pad_x, pady=6)

        # --- SECCIÓN 5: DESHACER (UNDO) Y PILA ---
        lbl_sec5 = tk.Label(
            self.panel_izq,
            text="HISTORIAL Y UNDO [Pila LIFO: O(1)]",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        )
        lbl_sec5.pack(anchor="w", padx=pad_x, pady=(4, 2))

        btn_undo = tk.Button(
            self.panel_izq,
            text="↩ Deshacer Último Comando (Undo)",
            font=("Segoe UI", 9, "bold"),
            bg="#f8fafc",
            fg="#475569",
            relief="solid",
            bd=1,
            cursor="hand2",
            pady=5,
            command=self.accion_deshacer,
        )
        btn_undo.pack(fill="x", padx=pad_x, pady=4)

        self.lbl_tope_pila = tk.Label(
            self.panel_izq,
            text="Tope: (Pila vacía)",
            font=("Segoe UI", 8, "italic"),
            bg=COLOR_PANEL,
            fg=COLOR_SUBTEXTO,
            wraplength=280,
            justify="left",
        )
        self.lbl_tope_pila.pack(anchor="w", padx=pad_x, pady=(2, 8))

    def _construir_panel_derecho(self):
        """Áreas gráficas divididas en Pista/Carreteo, Radar y Aterrizaje."""
        # 1. ZONA DE CARRETEO Y PISTA DE DESPEGUE (COLA FIFO)
        f_pista = tk.LabelFrame(
            self.panel_der,
            text=" 🛫 PISTA DE CARRETEO Y DESPEGUE [Cola FIFO - O(1)] ",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            bd=1,
            relief="solid",
        )
        f_pista.pack(fill="x", pady=(0, 10))

        # Canvas para dibujar la pista gráfica de asfalto y los aviones
        self.canvas_pista = tk.Canvas(
            f_pista, bg="#f1f5f9", height=115, highlightthickness=0
        )
        self.canvas_pista.pack(fill="x", padx=10, pady=8)

        # 2. RADAR DEL ESPACIO AÉREO (LISTA DOBLEMENTE ENLAZADA)
        f_radar = tk.LabelFrame(
            self.panel_der,
            text=" 🛰 ESPACIO AÉREO ACTIVO / RADAR [Lista Doblemente Enlazada - O(1)] ",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            bd=1,
            relief="solid",
        )
        f_radar.pack(fill="both", expand=True, pady=(0, 10))

        self.canvas_radar = tk.Canvas(
            f_radar, bg=COLOR_CIELO, highlightthickness=0
        )
        self.canvas_radar.pack(fill="both", expand=True, padx=10, pady=8)

        # 3. ZONA DE APROXIMACIÓN / COLA DE ATERRIZAJE (MIN-HEAP)
        f_heap = tk.LabelFrame(
            self.panel_der,
            text=" 🚨 APROXIMACIÓN DE ATERRIZAJE [Min-Heap / Prioridad - O(log n)] ",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            bd=1,
            relief="solid",
        )
        f_heap.pack(fill="x", pady=(0, 4))

        # Leyenda de colores de prioridad (colocada arriba para máxima visibilidad)
        self._crear_leyenda_prioridades(f_heap)

        self.canvas_heap = tk.Canvas(
            f_heap, bg="#fffbeb", height=90, highlightthickness=0
        )
        self.canvas_heap.pack(fill="x", padx=10, pady=(2, 8))

    def _crear_leyenda_prioridades(self, padre):
        """Muestra la referencia visual del significado de los colores 1 a 4 con insignias grandes."""
        f_leyenda = tk.Frame(padre, bg=COLOR_PANEL)
        f_leyenda.pack(fill="x", padx=10, pady=(6, 4))

        tk.Label(
            f_leyenda,
            text="Nivel de Prioridad:",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
        ).pack(side="left", padx=(0, 8))

        for nivel in (1, 2, 3, 4):
            cfg = COLORES_PRIORIDAD[nivel]
            box = tk.Label(
                f_leyenda,
                text=f"  {cfg['texto']}  ",
                font=("Segoe UI", 9, "bold"),
                bg=cfg["bg"],
                fg=cfg["fg"],
                padx=8,
                pady=4,
                relief="flat",
            )
            box.pack(side="left", padx=4)

    # -------------------------------------------------------------
    # RENDERIZADO VISUAL DE LAS ESTRUCTURAS DE DATOS
    # -------------------------------------------------------------

    def _dimensiones(self, canvas, def_w=800, def_h=100):
        """Obtiene las dimensiones reales del canvas evitando el ancho '1' de widgets recién inicializados."""
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 50:
            w = canvas.winfo_reqwidth()
        if w <= 50:
            w = def_w
        if h <= 20:
            h = canvas.winfo_reqheight()
        if h <= 20:
            h = def_h
        return w, h

    def actualizar_vistas(self):
        """Redibuja en tiempo real las 4 estructuras de datos."""
        self._dibujar_pista_despegue()
        self._dibujar_radar()
        self._dibujar_cola_aterrizajes()
        self._actualizar_info_pila()
        self._actualizar_combo_radar()

    def _dibujar_pista_despegue(self):
        """Dibuja la pista de asfalto y los nodos de la Cola FIFO sin sobreposiciones."""
        c = self.canvas_pista
        c.delete("all")
        ancho, alto = self._dimensiones(c, 800, 110)

        # Dibujar asfalto de la pista
        c.create_rectangle(15, 12, ancho - 15, alto - 12, fill=COLOR_PISTA, outline="#1e293b", width=2)

        # Zona de cabecera (Threshold con franjas blancas tipo piano)
        x_umbral = 80
        for y_franja in range(22, alto - 22, 14):
            c.create_rectangle(22, y_franja, 38, y_franja + 7, fill="#f8fafc", outline="")

        # Marcación de cabecera ("36R") con fondo limpio
        c.create_rectangle(44, alto // 2 - 14, 78, alto // 2 + 14, fill="#1e293b", outline="#475569")
        c.create_text(61, alto // 2, text="36R", fill="#ffffff", font=("Segoe UI", 9, "bold"))

        # Línea central punteada blanca (inicia DESPUÉS de la cabecera)
        c.create_line(86, alto // 2, ancho - 25, alto // 2, fill=COLOR_LINEA_PISTA, dash=(12, 10), width=2)

        vuelos = self.torre.despegues.listar()
        if not vuelos:
            # Cápsula limpia en el centro para evitar que la línea central atraviese el texto
            cx = (86 + ancho - 25) // 2
            cy = alto // 2
            c.create_rectangle(cx - 240, cy - 15, cx + 240, cy + 15, fill="#1e293b", outline="#475569", width=1)
            c.create_text(
                cx,
                cy,
                text="✈ Pista libre (Cola FIFO vacía - Ningún avión esperando despegue)",
                fill="#e2e8f0",
                font=("Segoe UI", 9, "italic"),
            )
            return

        # Renderizar cada avión en la cola (de izquierda a derecha: frente -> final)
        x_base = 96
        card_w = 115
        card_h = 52

        for i, vuelo in enumerate(vuelos):
            x1 = x_base + i * (card_w + 24)
            y1 = (alto - card_h) // 2
            x2 = x1 + card_w
            y2 = y1 + card_h

            if x2 > ancho - 30:
                restantes = len(vuelos) - i
                c.create_rectangle(ancho - 55, y1, ancho - 20, y2, fill="#1e293b", outline="#475569")
                c.create_text(
                    ancho - 37,
                    alto // 2,
                    text=f"+{restantes}",
                    fill="#ffffff",
                    font=("Segoe UI", 9, "bold"),
                )
                break

            # Tarjeta de avión
            cfg = COLORES_PRIORIDAD.get(vuelo.nivel_emergencia, COLORES_PRIORIDAD[4])
            c.create_rectangle(x1, y1, x2, y2, fill=COLOR_PANEL, outline=cfg["bg"], width=2)
            c.create_rectangle(x1, y1, x1 + 6, y2, fill=cfg["bg"], outline="")

            c.create_text(x1 + 14, y1 + 16, text=f"✈ {vuelo.codigo}", font=("Segoe UI", 9, "bold"), fill=COLOR_TEXTO, anchor="w")
            c.create_text(x1 + 14, y1 + 36, text=f"{vuelo.aerolinea} -> {vuelo.destino}", font=("Segoe UI", 8), fill=COLOR_SUBTEXTO, anchor="w")

            # Indicadores didácticos de punteros: frente y final
            if i == 0:
                c.create_text(x1 + card_w // 2, y1 - 8, text="▼ frente (sale primero)", fill="#38bdf8", font=("Segoe UI", 8, "bold"))
            if i == len(vuelos) - 1:
                c.create_text(x1 + card_w // 2, y2 + 8, text="▲ final (último)", fill="#fbbf24", font=("Segoe UI", 8, "bold"))

            # Flecha de enlace entre nodos
            if i < len(vuelos) - 1:
                xf1 = x2 + 3
                xf2 = x2 + 20
                c.create_line(xf1, alto // 2, xf2, alto // 2, fill="#38bdf8", arrow=tk.LAST, width=2)

    def _dibujar_radar(self):
        """Dibuja el espacio aéreo y la lista doblemente enlazada de vuelos activos."""
        c = self.canvas_radar
        c.delete("all")
        ancho, alto = self._dimensiones(c, 800, 240)

        # Anillos concéntricos del radar
        cx = ancho // 2
        cy = alto // 2
        for r in (60, 120, 180, 240):
            c.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#e0f2fe", width=1)
        c.create_line(cx, 10, cx, alto - 10, fill="#e0f2fe", dash=(4, 4))
        c.create_line(10, cy, ancho - 10, cy, fill="#e0f2fe", dash=(4, 4))

        vuelos = self.torre.radar.listar()
        if not vuelos:
            c.create_rectangle(cx - 180, cy - 25, cx + 180, cy + 25, fill="#ffffff", outline="#bae6fd", width=1)
            c.create_text(
                cx,
                cy,
                text="📡 Espacio aéreo despejado\n(Lista Doble vacía - Autoriza despegues para ver aviones en vuelo)",
                fill="#0284c7",
                font=("Segoe UI", 10, "italic"),
                justify="center",
            )
            return

        # Distribuir los vuelos visualmente en círculo o en línea enlazada
        n = len(vuelos)
        card_w = 120
        card_h = 56
        x_start = 40
        espacio = max(card_w + 35, (ancho - 80) // max(n, 1))

        for i, vuelo in enumerate(vuelos):
            # Posición escalonada para que no se superpongan
            x1 = x_start + i * espacio
            # Ondulación en Y para dar sensación de vuelo a diferentes altitudes
            y_offset = (i % 3 - 1) * 35
            y1 = max(20, min(alto - card_h - 20, cy - card_h // 2 + y_offset))
            x2 = x1 + card_w
            y2 = y1 + card_h

            cfg = COLORES_PRIORIDAD.get(vuelo.nivel_emergencia, COLORES_PRIORIDAD[4])

            # Tarjeta de vuelo
            tag_vuelo = f"vuelo_{vuelo.codigo}"
            c.create_rectangle(x1, y1, x2, y2, fill=COLOR_PANEL, outline=cfg["bg"], width=2, tags=(tag_vuelo,))
            c.create_rectangle(x1, y1, x2, y1 + 18, fill=cfg["bg"], outline="", tags=(tag_vuelo,))

            # Texto de la tarjeta
            c.create_text(
                x1 + 8, y1 + 9, text=f"✈ {vuelo.codigo}", fill=cfg["fg"], font=("Segoe UI", 9, "bold"), anchor="w", tags=(tag_vuelo,)
            )
            c.create_text(
                x1 + 8, y1 + 28, text=f"{vuelo.aerolinea} • {vuelo.destino}", fill=COLOR_TEXTO, font=("Segoe UI", 8), anchor="w", tags=(tag_vuelo,)
            )
            c.create_text(
                x1 + 8, y1 + 43, text=f"Estado: {vuelo.estado}", fill=COLOR_SUBTEXTO, font=("Segoe UI", 7, "bold"), anchor="w", tags=(tag_vuelo,)
            )

            # Doble flecha bidireccional entre nodos contiguos (demuestra Lista Doble)
            if i < n - 1:
                sig_x = x_start + (i + 1) * espacio
                sig_y = max(20, min(alto - card_h - 20, cy - card_h // 2 + ((i + 1) % 3 - 1) * 35))
                # Flechas dobles: anterior <--> siguiente
                c.create_line(x2 + 2, y1 + card_h // 2, sig_x - 2, sig_y + card_h // 2, fill="#0284c7", arrow=tk.BOTH, width=2)
                c.create_text((x2 + sig_x) // 2, (y1 + sig_y) // 2 - 10, text="prev/next", fill="#0284c7", font=("Segoe UI", 7, "italic"))

            # Permite hacer clic sobre el avión para seleccionarlo directamente en la torre
            c.tag_bind(tag_vuelo, "<Button-1>", lambda e, cod=vuelo.codigo: self.seleccionar_vuelo_radar(cod))

    def _dibujar_cola_aterrizajes(self):
        """Muestra los vuelos en la cola de aterrizaje según la prioridad del Min-Heap."""
        c = self.canvas_heap
        c.delete("all")
        ancho, alto = self._dimensiones(c, 800, 90)

        heap_vuelos = self.torre.aterrizajes.datos
        if not heap_vuelos:
            c.create_text(
                ancho // 2,
                alto // 2,
                text="🛬 Rampa de aproximación libre (Min-Heap vacío - No hay vuelos con solicitud de aterrizaje)",
                fill="#94a3b8",
                font=("Segoe UI", 10, "italic"),
            )
            return

        # El primer elemento (índice 0) siempre es la raíz del Heap = más prioritario
        x_base = 25
        card_w = 145
        card_h = 55

        for i, vuelo in enumerate(heap_vuelos):
            x1 = x_base + i * (card_w + 20)
            y1 = (alto - card_h) // 2
            x2 = x1 + card_w
            y2 = y1 + card_h

            if x2 > ancho - 30:
                c.create_text(ancho - 30, alto // 2, text=f"+{len(heap_vuelos) - i}...", fill=COLOR_TEXTO, font=("Segoe UI", 9, "bold"))
                break

            cfg = COLORES_PRIORIDAD.get(vuelo.nivel_emergencia, COLORES_PRIORIDAD[4])

            # Fondo destacado si es la raíz del Heap
            es_raiz = (i == 0)
            borde_ancho = 3 if es_raiz else 1
            borde_color = "#b91c1c" if es_raiz else cfg["bg"]

            c.create_rectangle(x1, y1, x2, y2, fill=COLOR_PANEL, outline=borde_color, width=borde_ancho)
            c.create_rectangle(x1, y1, x2, y1 + 18, fill=cfg["bg"], outline="")

            # Título de la tarjeta
            c.create_text(
                x1 + 6, y1 + 9, text=f"🚨 {vuelo.codigo} ({cfg['texto'].split('-')[0].strip()})", fill=cfg["fg"], font=("Segoe UI", 8, "bold"), anchor="w"
            )
            c.create_text(x1 + 6, y1 + 28, text=f"{vuelo.aerolinea} -> {vuelo.destino}", fill=COLOR_TEXTO, font=("Segoe UI", 8), anchor="w")

            if es_raiz:
                c.create_text(x1 + card_w // 2, y2 + 8, text="★ Raíz: Próximo en Aterrizar", fill="#b91c1c", font=("Segoe UI", 8, "bold"))
            else:
                c.create_text(x1 + card_w // 2, y2 + 8, text=f"Pos. Heap [{i}]", fill=COLOR_SUBTEXTO, font=("Segoe UI", 7))

    def _actualizar_info_pila(self):
        """Actualiza la etiqueta con el comando en el tope de la Pila LIFO."""
        tope = self.torre.historial.peek()
        total = len(self.torre.historial)
        if tope is None:
            self.lbl_tope_pila.config(text=f"Tope: (Pila vacía) | Total: 0")
        else:
            tipo, vuelo = tope
            self.lbl_tope_pila.config(
                text=f"Tope: {tipo} -> {vuelo.codigo} | Total: {total} comandos"
            )

    def _actualizar_combo_radar(self):
        """Rellena el selector con los vuelos actualmente en vuelo en el radar."""
        vuelos_radar = [v.codigo for v in self.torre.radar.listar() if v.estado == "EN_VUELO"]
        self.combo_radar["values"] = vuelos_radar
        if vuelos_radar and not self.combo_radar.get():
            self.combo_radar.current(0)
        elif not vuelos_radar:
            self.combo_radar.set("")

    def seleccionar_vuelo_radar(self, codigo):
        """Al hacer clic sobre un avión en el radar, lo carga automáticamente en el combo."""
        self.combo_radar.set(codigo)

    # -------------------------------------------------------------
    # CONTROLADORES DE EVENTOS / ACCIONES
    # -------------------------------------------------------------

    def accion_pedir_despegue(self):
        codigo = self.txt_codigo.get().strip().upper()
        aerolinea = self.txt_aerolinea.get().strip()
        destino = self.txt_destino.get().strip().upper()

        if not codigo or not aerolinea or not destino:
            messagebox.showwarning("Datos Incompletos", "Por favor completa código, aerolínea y destino.")
            return

        vuelo = self.torre.pedir_despegue(codigo, aerolinea, destino)
        self.actualizar_vistas()
        # Generar sugerencia de código para el siguiente
        num = random.randint(100, 999)
        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, f"AV{num}")

    def accion_despegar(self):
        vuelo = self.torre.despegar()
        if vuelo is None:
            messagebox.showinfo("Pista Vacía", "No hay aviones en la cola de despegue esperando pista.")
            return
        self.actualizar_vistas()

    def accion_solicitar_aterrizaje(self):
        codigo = self.combo_radar.get().strip()
        if not codigo:
            messagebox.showwarning("Vuelo No Seleccionado", "Selecciona un vuelo activo en el radar.")
            return

        raw_nivel = self.combo_nivel.get()
        nivel = int(raw_nivel.split(" - ")[0])

        vuelo = self.torre.solicitar_aterrizaje(codigo, nivel)
        if vuelo is None:
            messagebox.showerror("Error", f"El vuelo {codigo} no se encuentra en el radar o no está en estado EN_VUELO.")
            return

        self.actualizar_vistas()

    def accion_aterrizar(self):
        vuelo = self.torre.aterrizar()
        if vuelo is None:
            messagebox.showinfo("Rampa Libre", "No hay vuelos en la cola de aterrizaje solicitando pista.")
            return
        self.actualizar_vistas()
        messagebox.showinfo(
            "Aterrizaje Exitoso",
            f"El vuelo {vuelo.codigo} ({vuelo.aerolinea}) ha aterrizado con éxito.\n"
            f"Prioridad atendida: Nivel {vuelo.nivel_emergencia}",
        )

    def accion_deshacer(self):
        cmd = self.torre.deshacer()
        if cmd is None:
            messagebox.showinfo("Pila Vacía", "No hay comandos en el historial para deshacer.")
            return
        tipo, vuelo = cmd
        self.actualizar_vistas()
        messagebox.showinfo("Comando Deshecho", f"Se deshizo la operación:\n{tipo} de {vuelo.codigo}")

    def cargar_vuelo_demo(self):
        """Inyecta un vuelo aleatorio a la cola para facilitar la sustentación en vivo."""
        prefijo, aerolinea, destino = random.choice(AEROLINEAS_DEMO)
        self.contador_demo += 1
        codigo = f"{prefijo}{self.contador_demo}"
        self.torre.pedir_despegue(codigo, aerolinea, destino)
        self.actualizar_vistas()


def main():
    root = tk.Tk()
    app = InterfazSkyFlow(root)
    # Redibujar cuando cambie el tamaño de ventana
    root.bind("<Configure>", lambda e: app.actualizar_vistas() if e.widget == root else None)
    # Redibujar tras el mapeo inicial de Windows para asegurar el ancho total
    root.after(100, app.actualizar_vistas)
    root.mainloop()


if __name__ == "__main__":
    main()
