# 📘 Manual de Usuario - SkyFlow (Control de Tráfico Aéreo)

Bienvenido al manual de usuario de **SkyFlow**, un simulador de torre de control de tráfico aéreo diseñado con fines pedagógicos para la materia de **Estructuras de Datos**.

---

## 📑 Tabla de Contenidos
1. [Introducción y Propósito](#1-introducción-y-propósito)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Cómo Iniciar la Aplicación](#3-cómo-iniciar-la-aplicación)
4. [Ciclo de Vida de un Vuelo](#4-ciclo-de-vida-de-un-vuelo)
5. [Guía de la Interfaz Gráfica (GUI)](#5-guía-de-la-interfaz-gráfica-gui)
6. [Guía del Modo Terminal / Consola](#6-guía-del-modo-terminal--consola)
7. [Atajos y Herramientas Útiles](#7-atajos-y-herramientas-útiles)
8. [Preguntas Frecuentes y Solución de Problemas](#8-preguntas-frecuentes-y-solución-de-problemas)
9. [Ejecución de Pruebas Unitarias](#9-ejecución-de-pruebas-unitarias)

---

## 1. Introducción y Propósito

**SkyFlow** permite coordinar el tráfico aéreo en un aeropuerto mediante 4 operaciones clave, cada una respaldada por una estructura de datos clásica implementada desde cero:

* **Pista de Carreteo y Despegue:** Gestionada por una **Cola FIFO** ($O(1)$) donde el primer avión en llegar es el primero en despegar.
* **Espacio Aéreo (Radar):** Gestionado por una **Lista Doblemente Enlazada** ($O(1)$) que monitorea los aviones en vuelo.
* **Aproximación y Aterrizaje:** Gestionado por un **Min-Heap (Cola de Prioridad)** ($O(\log n)$) que prioriza aterrizajes según la gravedad de la emergencia.
* **Historial de Operaciones:** Gestionado por una **Pila LIFO** ($O(1)$) que permite revertir (*Undo*) comandos ejecutados.

---

## 2. Requisitos del Sistema

* **Sistema Operativo:** Windows 10/11 (compatible también con Linux y macOS).
* **Python:** Versión 3.10 o superior (verificar con `python --version`).
* **Librerías externas:** **Ninguna.** Todo el proyecto funciona con Python estándar (`tkinter`, `unittest`).

---

## 3. Cómo Iniciar la Aplicación

Existen dos modalidades principales para abrir SkyFlow:

### Opción A: Acceso Rápido con Doble Clic (Windows)
En la carpeta raíz del proyecto encontrarás dos ejecutables directos:
* ✈ **`Iniciar_SkyFlow_Grafico.bat`**: Abre directamente la interfaz gráfica maximizada.
* 💻 **`Iniciar_SkyFlow_Consola.bat`**: Abre la consola interactiva en una ventana dedicada.

### Opción B: Desde la Terminal (CMD o PowerShell)
Abre tu terminal y ubícate en la carpeta del proyecto:
```cmd
cd /d "g:\My Drive\UNAL\2026-2\Estructuras\SkyFlow"
```
Luego ejecuta:
* Para la interfaz gráfica:
  ```cmd
  python gui.py
  ```
* Para la consola interactiva:
  ```cmd
  python main.py
  ```

---

## 4. Ciclo de Vida de un Vuelo

Para operar la torre de control correctamente, ten en cuenta el flujo lógico de los aviones:

```
[1. Encolar Despegue]  ──▶  Fila de Pista (Cola FIFO)      [Estado: EN_ESPERA]
                                    │
[2. Autorizar Despegue]             ▼
                             Radar Aéreo (Lista Doble)     [Estado: EN_VUELO]
                                    │
[3. Solicitar Aterrizaje]           ▼
                             Rampa Heap (Min-Heap)         [Estado: ESPERANDO_ATERRIZAJE]
                                    │
[4. Aterrizar Prioritario]          ▼
                             Aterrizado (Sale del radar)   [Estado: ATERRIZADO]
```

> ⚠️ **Regla importante:** Un avión **solo** puede solicitar aterrizaje si ya despegó y se encuentra activo en el radar (`EN_VUELO`).

---

## 5. Guía de la Interfaz Gráfica (GUI)

La interfaz se divide en dos secciones principales: el **Panel de Control** (izquierda) y el **Visualizador de Estructuras** (derecha).

### 5.1 Panel de Control (Izquierda)

1. **Registrar en Pista [Cola FIFO]:**
   * Ingresa el código (ej. `AV101`), aerolínea (ej. `Avianca`) y destino (ej. `MDE`).
   * Haz clic en **`+ Encolar para Despegue (O(1))`**.
2. **Autorizar Despegue:**
   * Haz clic en **`🛫 Despegar Siguiente (FIFO ➔ Radar)`**.
   * El avión en el `frente` de la cola saldrá de la pista y pasará al radar aéreo.
3. **Solicitar Aterrizaje / Emergencia:**
   * Selecciona un vuelo del menú desplegable (o haz clic sobre él directamente en el radar).
   * Selecciona el nivel de prioridad:
     * **N1 - Crítico (Mayday) [Rojo]:** Falla catastrófica / Mayday.
     * **N2 - Combustible Bajo [Naranja]:** Poca autonomía.
     * **N3 - Falla Técnica [Amarillo]:** Problemas menores en sistemas.
     * **N4 - Normal [Verde]:** Aterrizaje programado estándar.
   * Haz clic en **`🚨 Insertar en Cola de Aterrizaje (Min-Heap)`**.
4. **Pista de Aterrizaje:**
   * Haz clic en **`🛬 Aterrizar Más Urgente (O(log n))`**.
   * El avión con menor número de prioridad (más crítico) aterrizará primero y saldrá del radar.
5. **Historial y Deshacer (Undo) [Pila LIFO]:**
   * Muestra el comando en el tope de la pila.
   * Haz clic en **`↩ Deshacer Último Comando (Undo)`** para revertir la última acción realizada.

### 5.2 Visualizador de Estructuras (Derecha)

* **🛫 Pista de Carreteo y Despegue:** Muestra la pista de asfalto (`36R`). Verás las etiquetas didácticas `▼ frente` (próximo a despegar) y `▲ final` (último encolado), además de las flechas del enlace FIFO.
* **🛰 Espacio Aéreo Activo / Radar:** Muestra los aviones volando. Las flechas dobles `prev/next` evidencian los punteros de la lista doblemente enlazada. **Consejo:** Puedes hacer clic sobre cualquier avión para seleccionarlo automáticamente.
* **🚨 Aproximación de Aterrizaje:** Muestra los vuelos organizados por el Min-Heap. El nodo raíz (`[0]`) siempre estará destacado como el próximo en aterrizar.

---

## 6. Guía del Modo Terminal / Consola

Si prefieres la terminal interactiva (`python main.py`), verás el menú numérico:

```text
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
0. Salir
```

### Ejemplo de sesión en terminal:
1. Presiona `1` e ingresa: `AV101`, `Avianca`, `BOG`.
2. Presiona `2` para autorizar el despegue.
3. Presiona `6` para verificar que el avión aparece en el radar.
4. Presiona `3`, ingresa `AV101` y nivel de emergencia `1`.
5. Presiona `4` para aterrizarlo.
6. Presiona `8` para deshacer el aterrizaje si te equivocaste.

---

## 7. Atajos y Herramientas Útiles

| Atajo / Botón | Dónde usarlo | Acción |
| :--- | :--- | :--- |
| **`F11`** | Interfaz Gráfica | Alternar pantalla completa total (*Kiosk mode*). |
| **`Escape`** | Interfaz Gráfica | Salir de pantalla completa total. |
| **`⚡ Cargar Vuelo Demo`** | Barra superior GUI | Inyecta un vuelo aleatorio instantáneamente para pruebas en vivo. |
| **Clic sobre avión** | Radar GUI | Selecciona el vuelo en el formulario de aterrizaje. |
| **Opción `G`** | Menú Consola | Abre la ventana gráfica directamente desde la terminal. |

---

## 8. Preguntas Frecuentes y Solución de Problemas

### ❓ "Ese vuelo no está volando" al solicitar aterrizaje
* **Causa:** Intentaste solicitar aterrizaje para un vuelo que todavía está en la fila de carreteo o que no existe.
* **Solución:** Primero autoriza su despegue con el botón **Despegar** para que entre al radar (`EN_VUELO`).

### ❓ En Windows CMD el comando `cd` no cambia de carpeta
* **Causa:** En la consola de Windows clásica (CMD), cambiar de disco requiere el modificador `/d`.
* **Solución:** Escribe `cd /d "g:\My Drive\UNAL\2026-2\Estructuras\SkyFlow"` o ejecuta directamente el archivo `.bat`.

### ❓ ¿Qué pasa si declaro dos emergencias con igual prioridad?
* El Min-Heap extraerá de manera eficiente una de las emergencias equivalentes garantizando siempre complejidad $O(\log n)$.

---

## 9. Ejecución de Pruebas Unitarias

Para comprobar la integridad matemática y algorítmica de todas las estructuras de datos:

```cmd
python -m unittest discover -s tests -v
```

Verás las **26 pruebas automáticas** ejecutándose en menos de 0.05 segundos con resultado `OK`.
