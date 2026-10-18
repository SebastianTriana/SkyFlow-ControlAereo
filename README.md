#  SkyFlow - Sistema de Control de Tráfico Aéreo

---

##  Descripción del Proyecto

**SkyFlow** simula las operaciones de una torre de control de tráfico aéreo mediante la orquestación de 4 estructuras de datos fundamentales implementadas explícitamente con clases de nodos, punteros y arreglos base:

1. **Pista de Carreteo y Despegues:** Orden estricto de llegada de las aeronaves.
2. **Radar del Espacio Aéreo:** Seguimiento y monitoreo bidireccional de los vuelos activos en el aire.
3. **Aproximación de Aterrizaje:** Gestión de emergencias y prioridades de aterrizaje aeronáutico.
4. **Historial de la Torre de Control:** Registro de comandos y funcionalidad de deshacer (*undo*).

---

##  Estructuras de Datos Implementadas

Todas las estructuras se implementaron de forma explícita sin recurrir a colecciones ocultas del lenguaje (`queue.Queue`, `collections.deque` o `.pop(0)`):

| Estructura | Archivo | Rol en el Sistema | Operaciones Clave | Complejidad Big-O |
| :--- | :--- | :--- | :--- | :---: |
| **Cola (`Queue`)** | [`estructuras/cola_fifo.py`](estructuras/cola_fifo.py) | Fila de carreteo y pista de despegue | `enqueue`, `dequeue`, `peek` | **$O(1)$** |
| **Lista Doblemente Enlazada (`DoublyLinkedList`)** | [`estructuras/lista_doble.py`](estructuras/lista_doble.py) | Radar de aeronaves en el espacio aéreo | `insert`, `remove(nodo)` | **$O(1)$** |
| **Min-Heap (`PriorityQueue`)** | [`estructuras/cola_prioridad.py`](estructuras/cola_prioridad.py) | Rampa de aproximación por criticidad de emergencia | `insert`, `extract_min` | **$O(\log n)$** |
| **Pila (`Stack`)** | [`estructuras/pila_lifo.py`](estructuras/pila_lifo.py) | Historial de la torre y función Deshacer (*undo*) | `push`, `pop`, `peek` | **$O(1)$** |

### Semáforo de Prioridades de Aterrizaje
- 🔴 **Nivel 1 (Crítico / Mayday):** Emergencia máxima (fallo de motor, despresurización).
- 🟠 **Nivel 2 (Combustible Bajo):** Prioridad alta por autonomía limitada.
- 🟡 **Nivel 3 (Falla Técnica):** Desvío de ruta o fallo menor.
- 🟢 **Nivel 4 (Normal):** Vuelo regular sin incidencias.

---

##  Estructura del Repositorio

```text
SkyFlow/
├── estructuras/              # Módulos de estructuras de datos
│   ├── cola_fifo.py          # Cola con punteros frente y final (O(1))
│   ├── lista_doble.py        # Nodos con punteros anterior y siguiente (O(1))
│   ├── cola_prioridad.py     # Min-Heap binario sobre lista base (O(log n))
│   └── pila_lifo.py          # Pila con puntero al tope (O(1))
├── modelos/                  # Entidades de dominio
│   └── vuelo.py              # Clase Vuelo (código, aerolínea, emergencia, estado)
├── tests/                    # Suite de pruebas unitarias
│   ├── test_despegues.py
│   ├── test_lista_doble.py
│   ├── test_cola_prioridad.py
│   ├── test_pila.py
│   └── test_simulador.py
├── simulador.py              # Controlador de la torre (orquestador de estructuras)
├── gui.py                    # Interfaz gráfica de usuario en Tkinter (Modo Claro)
├── main.py                   # Menú interactivo de consola
├── Iniciar_SkyFlow_Grafico.bat # Lanzador de doble clic para la GUI
├── Iniciar_SkyFlow_Consola.bat # Lanzador de doble clic para la consola
├── MANUAL_USUARIO.md         # Manual de usuario con ejemplos y guía de capturas
├── ESTRUCTURAS_EXPLICACION.md # Justificación teórica y análisis Big-O
└── README.md
```

---

##  Documentación Formal del Proyecto

Para la revisión y sustentación académica detallada, consulta los documentos complementarios:

*  [**Manual de Usuario (`MANUAL_USUARIO.md`)**](MANUAL_USUARIO.md): Guía paso a paso para ejecutar el sistema por consola y GUI, con ejemplos prácticos de entrada/salida y marcadores visuales para capturas de pantalla.
*  [**Explicación de Estructuras de Datos (`ESTRUCTURAS_EXPLICACION.md`)**](ESTRUCTURAS_EXPLICACION.md): Justificación teórica y práctica de las 4 estructuras, tabla de complejidades Big-O completa, argumentación de optimalidad frente a arreglos tradicionales y diagramas de punteros en memoria.

---

##  Cómo Ejecutar el Proyecto

El proyecto requiere **Python 3.10 o superior** y no necesita instalar ninguna librería externa (`pip`).

### Opción 1: Lanzadores Directos de Windows (Recomendada)
- Haz doble clic en **`Iniciar_SkyFlow_Grafico.bat`** para abrir la interfaz gráfica maximizada.
- Haz doble clic en **`Iniciar_SkyFlow_Consola.bat`** para abrir la torre de control en la terminal.

### Opción 2: Desde la Terminal (PowerShell / CMD)
Asegúrate de estar en la carpeta del proyecto:
```bash
# Iniciar la interfaz gráfica (Modo Claro)
python gui.py

# O iniciar la consola interactiva
python main.py
```

> **Atajos en la GUI:**
> - Presiona **`F11`** para alternar a pantalla completa sin bordes.
> - Presiona **`Escape`** para regresar al modo maximizado estándar.
> - Haz clic en el botón **`⚡ Cargar Vuelo Demo`** para inyectar tráfico aéreo de prueba instantáneo.

---

##  Pruebas Unitarias

Para ejecutar el conjunto completo de las 26 pruebas automatizadas:

```bash
python -m unittest discover -s tests -v
```

---

##  Declaración de Metodología y Uso de Inteligencia Artificial

En concordancia con las buenas prácticas éticas y académicas en la formación universitaria de ingeniería de sistemas y computación, se declara formalmente la distribución metodológica del trabajo y el uso de herramientas de asistencia en el desarrollo de **SkyFlow**:

* **70% Asistencia de Herramientas de IA (Google Antigravity / Claude Sonnet):**
  * Generación y refinamiento iterativo de código base de estructuras de datos con diseño limpio y modular.
  * Construcción de la interfaz gráfica interactiva en `tkinter` y cálculo reactivo de dimensiones en canvas.
  * Elaboración de la suite de pruebas unitarias y redacción de esquemas de documentación técnica y manuales en Markdown.
* **30% Desarrollo, Diseño, Auditoría y Validación por el Estudiante:**
  * Concepción y diseño conceptual de la arquitectura de la torre de control y selección de las cuatro estructuras de datos.
  * Definición estricta de requerimientos y restricciones algorítmicas (implementación mediante nodos, punteros y sin colecciones ocultas).
  * Inspección, auditoría y revisión manual línea por línea del código fuente generado para garantizar su legibilidad, corrección sintáctica y facilidad de sustentación en vivo.
  * Pruebas funcionales en tiempo real, validación de la experiencia de usuario y resolución de casos de borde en Windows.


