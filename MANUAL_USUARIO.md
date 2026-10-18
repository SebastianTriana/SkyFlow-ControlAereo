#  Manual de Usuario - SkyFlow (Control de Tráfico Aéreo)

> **Documentación Oficial de Usuario para Entrega Académica**  
> **Asignatura:** Estructuras de Datos  
> **Institución:** Universidad Nacional de Colombia  

---

##  Tabla de Contenidos
1. [Introducción al Sistema](#1-introducción-al-sistema)
2. [Requisitos y Formas de Ejecución](#2-requisitos-y-formas-de-ejecución)
   - [2.1 Lanzadores Directos de Windows (.bat)](#21-lanzadores-directos-de-windows-bat)
   - [2.2 Ejecución por Consola de Comandos](#22-ejecución-por-consola-de-comandos)
3. [Guía Detallada del Modo Consola (`main.py`)](#3-guía-detallada-del-modo-consola-mainpy)
   - [Opción 1: Pedir Despegue](#opción-1-pedir-despegue)
   - [Opción 2: Despegar Siguiente](#opción-2-despegar-siguiente)
   - [Opción 3: Solicitar Aterrizaje / Emergencia](#opción-3-solicitar-aterrizaje--declarar-emergencia)
   - [Opción 4: Aterrizar el Más Urgente](#opción-4-aterrizar-el-más-urgente)
   - [Opción 5: Ver Fila de Despegue](#opción-5-ver-fila-de-despegue)
   - [Opción 6: Ver Radar](#opción-6-ver-radar)
   - [Opción 7: Ver Cola de Aterrizaje](#opción-7-ver-cola-de-aterrizaje)
   - [Opción 8: Deshacer Último Comando](#opción-8-deshacer-último-comando-undo)
   - [Opción 9: Ver Historial](#opción-9-ver-historial)
   - [Opción G: Abrir Interfaz Gráfica](#opción-g-abrir-interfaz-gráfica-tkinter)
   - [Opción 0: Salir](#opción-0-salir)
4. [Guía Detallada de la Interfaz Gráfica (`gui.py`)](#4-guía-detallada-de-la-interfaz-gráfica-guipy)
   - [4.1 Distribución General de la Pantalla](#41-distribución-general-de-la-pantalla)
   - [4.2 Operaciones Paso a Paso en la GUI](#42-operaciones-paso-a-paso-en-la-gui)
   - [4.3 Interpretación Visual de Estructuras de Datos](#43-interpretación-visual-de-estructuras-de-datos)
5. [Atajos de Teclado y Ayudas de Sustentación](#5-atajos-de-teclado-y-ayudas-de-sustentación)
6. [Resolución de Problemas Frecuentes](#6-resolución-de-problemas-frecuentes)

---

## 1. Introducción al Sistema

**SkyFlow** es un simulador interactivo de control de tráfico aéreo. Su objetivo es modelar con fidelidad algorítmica las operaciones críticas de un aeropuerto:

* **Encolamiento en pista:** Garantizar justicia de salida por orden de llegada (FIFO).
* **Vuelos en tránsito:** Monitoreo y trazabilidad bidireccional de los aviones en el aire.
* **Aterrizajes de emergencia:** Priorización dinámica del avión en mayor peligro de combustible o falla técnica sobre vuelos ordinarios.
* **Control de errores de torre:** Capacidad de revertir comandos erróneos en orden inverso a su ejecución (LIFO).

El sistema ofrece dos modalidades de uso intercambiables que comparten el mismo estado y lógica de negocio: **Consola de Texto** e **Interfaz Gráfica (Tkinter)**.

---

## 2. Requisitos y Formas de Ejecución

### Requisitos Previos
* **Python 3.10 o superior** instalado en el sistema.
* No se requiere instalar librerías externas mediante `pip` (cero dependencias).

---

### 2.1 Lanzadores Directos de Windows (.bat)
Para usuarios en Windows, la forma más rápida y recomendada es utilizar los archivos ejecutables ubicados en la raíz del proyecto:

1. **`Iniciar_SkyFlow_Grafico.bat`**: Al hacer doble clic, abre la aplicación gráfica en pantalla completa/maximizada.
2. **`Iniciar_SkyFlow_Consola.bat`**: Al hacer doble clic, abre una ventana de comando dedicada con el menú textual de la torre de control.

> [!NOTE]
> Estos lanzadores están programados con `%~dp0`, por lo que funcionan en cualquier disco o memoria USB sin importar la ruta donde se guarde la carpeta.

---

### 2.2 Ejecución por Consola de Comandos
Si ejecutas desde una terminal (CMD o PowerShell), navega al directorio del proyecto.


* Para iniciar el **modo consola**:
  ```cmd
  python main.py
  ```
* Para iniciar el **modo gráfico**:
  ```cmd
  python gui.py
  ```

---

## 3. Guía Detallada del Modo Consola (`main.py`)

Al iniciar `main.py`, se despliega el menú principal interactivo:

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

<img width="383" height="270" alt="image" src="https://github.com/user-attachments/assets/5cc91928-5f71-49ff-8344-73b68153f131" />

---

### Opción 1: Pedir Despegue
Registra una aeronave en la fila de carreteo de la pista (Cola FIFO).

* **Entradas solicitadas:**
  * Código de vuelo (ej. `AV101`)
  * Nombre de aerolínea (ej. `Avianca`)
  * Aeropuerto de destino (ej. `MDE`)
* **Ejemplo práctico de interacción:**
  ```text
  Opción: 1
  Código: AV101
  Aerolínea: Avianca
  Destino: MDE
  En fila: [AV101 | Avianca -> MDE | Prioridad: 4 | Estado: EN_ESPERA]
  ```
* **Efecto en el sistema:** El vuelo queda con estado `EN_ESPERA` y se posiciona al final de la Cola FIFO ($O(1)$).

---

### Opción 2: Despegar Siguiente
Autoriza el despegue de la aeronave que se encuentra en el **frente** de la fila de carreteo.

* **Ejemplo práctico de interacción:**
  ```text
  Opción: 2
  Despegó: [AV101 | Avianca -> MDE | Prioridad: 4 | Estado: EN_VUELO]
  ```
* **Efecto en el sistema:** El vuelo sale de la Cola FIFO (`dequeue`), su estado cambia a `EN_VUELO` y se inserta en la Lista Doblemente Enlazada del Radar ($O(1)$).
* **Caso de pista vacía:** Si no hay aeronaves, responde: `No hay vuelos disponibles.`

---

### Opción 3: Solicitar Aterrizaje / Declarar Emergencia
Permite que un avión que ya se encuentra en el aire solicite pista para aterrizar, indicando su nivel de urgencia aeronáutica.

* **Escala de prioridades:**
  * `1`: Crítico / Mayday (fallo de motor, despresurización).
  * `2`: Combustible bajo (autonomía limitada).
  * `3`: Falla técnica menor.
  * `4`: Vuelo normal programado.
* **Ejemplo práctico de interacción:**
  ```text
  Opción: 3
  Código del vuelo en el radar: AV101
  Nivel de emergencia (1 = crítico ... 4 = normal): 1
  Solicitud registrada: [AV101 | Avianca -> MDE | Prioridad: 1 | Estado: ESPERANDO_ATERRIZAJE]
  ```
* **Validación de seguridad:** Si el código ingresado no existe en el radar o no está volando, el sistema rechaza la solicitud:
  ```text
  Ese vuelo no está volando.
  ```

---

### Opción 4: Aterrizar el Más Urgente
Asigna la pista al vuelo que posee la máxima prioridad (menor valor numérico de emergencia) en el Min-Heap.

* **Ejemplo práctico de interacción:**
  ```text
  Opción: 4
  Aterrizó: [AV101 | Avianca -> MDE | Prioridad: 1 | Estado: ATERRIZADO]
  ```
* **Efecto en el sistema:** Se extrae la raíz del Heap (`extract_min` en $O(\log n)$), el vuelo cambia su estado a `ATERRIZADO` y se desvincula del radar en $O(1)$.

<img width="554" height="91" alt="image" src="https://github.com/user-attachments/assets/6933157e-35dc-4277-a4b7-587ff3e43629" />

<img width="547" height="45" alt="image" src="https://github.com/user-attachments/assets/0bb265b1-6397-401d-a8ba-02b885aa689f" />

<img width="748" height="79" alt="image" src="https://github.com/user-attachments/assets/409da8de-646d-4dfd-ad7b-ab4ced287bfa" />

<img width="562" height="40" alt="image" src="https://github.com/user-attachments/assets/e4bee626-9054-48f3-b0e3-1fe351e91170" />

---

### Opción 5: Ver Fila de Despegue
Imprime la lista de aeronaves formadas en la pista en estricto orden de salida (de izquierda/frente a derecha/final).

* **Ejemplo de salida:**
  ```text
  --- Fila de despegue (2) ---
  [AV101 | Avianca -> MDE | Prioridad: 4 | Estado: EN_ESPERA]
  [LA202 | LATAM -> LIM | Prioridad: 4 | Estado: EN_ESPERA]
  ```

---

### Opción 6: Ver Radar
Lista los vuelos que se encuentran navegando activamente en el espacio aéreo.

* **Ejemplo de salida:**
  ```text
  --- Radar (2) ---
  [AV101 | Avianca -> MDE | Prioridad: 4 | Estado: EN_VUELO]
  [AA901 | American -> MIA | Prioridad: 4 | Estado: EN_VUELO]
  ```

---

### Opción 7: Ver Cola de Aterrizaje
Muestra la representación interna del arreglo que almacena el Min-Heap de aterrizajes.

* **Ejemplo de salida:**
  ```text
  --- Cola de aterrizaje (orden interno del heap) (2) ---
  [AV101 | Avianca -> MDE | Prioridad: 1 | Estado: ESPERANDO_ATERRIZAJE]
  [IB602 | Iberia -> MAD | Prioridad: 3 | Estado: ESPERANDO_ATERRIZAJE]
  ```

---

### Opción 8: Deshacer Último Comando (Undo)
Revierta la última acción operativa ejecutada por la torre mediante la Pila LIFO.

* **Ejemplo práctico de interacción:**
  ```text
  Opción: 8
  Deshecho: ATERRIZAR AV101
  ```
* **Comportamiento reversible:**
  * Si se deshace un **Aterrizaje**, el avión vuelve al radar y a la cola de aproximación.
  * Si se deshace una **Solicitud**, el avión vuelve a estado regular en vuelo.
  * Si se deshace un **Despegue**, el avión sale del radar y vuelve al frente de la cola de pista.
  * Si se deshace un **Registro**, el avión se elimina de la cola.
* **Pila vacía:** Si no hay comandos previos: `Nada que deshacer.`

---

### Opción 9: Ver Historial
Imprime la pila completa de comandos almacenados, desde el más reciente (tope) hasta el más antiguo.

* **Ejemplo de salida:**
  ```text
  SOLICITAR_ATERRIZAJE -> AV101
  DESPEGAR -> AV101
  PEDIR_DESPEGUE -> AV101
  ```

<img width="374" height="512" alt="image" src="https://github.com/user-attachments/assets/c1c7c347-d086-4fc3-9d2d-145fb87486fc" />


---

### Opción G: Abrir Interfaz Gráfica (Tkinter)
Permite abrir la ventana visual de SkyFlow directamente desde la sesión en consola sin reiniciar el programa.

---

### Opción 0: Salir
Finaliza la ejecución del simulador en consola.

---

## 4. Guía Detallada de la Interfaz Gráfica (`gui.py`)

La interfaz gráfica fue concebida en **Modo Claro** para ofrecer una visibilidad óptima en proyectores y pantallas.

<img width="1366" height="723" alt="image" src="https://github.com/user-attachments/assets/f00f9a1c-b91a-4496-8f8e-83ab39e6dd86" />


---

### 4.1 Distribución General de la Pantalla

1. **Barra Superior:** Contiene el título del sistema y el botón didáctico **`⚡ Cargar Vuelo Demo`**, que permite inyectar vuelos aleatorios al instante durante la exposición.
2. **Panel Lateral Izquierdo (Acciones de Torre):**
   * Formulario de Registro rápido (Código, Aerolínea, Destino).
   * Botón de Autorización de Despegue.
   * Menú de Declaración de Emergencias con selector de vuelos en radar y nivel de gravedad (1 a 4).
   * Botón de Aterrizaje del vuelo más urgente.
   * Panel de Deshacer (*Undo*) con monitor del comando en el tope de la Pila.
3. **Panel Central / Derecho (Lienzo de Estructuras de Datos):**
   * **Pista de Carreteo y Despegue (Cola FIFO).**
   * **Espacio Aéreo / Radar (Lista Doblemente Enlazada).**
   * **Rampa de Aproximación (Min-Heap / Prioridad).**

---

### 4.2 Operaciones Paso a Paso en la GUI

#### Paso A: Encolar Aviones en la Pista
1. En el panel izquierdo, llena los campos o presiona el botón **`⚡ Cargar Vuelo Demo`** (arriba a la derecha).
2. Haz clic en **`+ Encolar para Despegue (O(1))`**.
3. Verás aparecer inmediatamente la tarjeta del avión sobre la pista de asfalto.


<img width="1015" height="170" alt="image" src="https://github.com/user-attachments/assets/a40a2976-901f-464f-a07e-0cf93de8efda" />


---

#### Paso B: Autorizar Despegues
1. Haz clic en **`🛫 Despegar Siguiente (FIFO ➔ Radar)`**.
2. El avión en el `frente` saldrá de la pista y aparecerá automáticamente flotando en el círculo del **Radar**.

---

#### Paso C: Declarar Emergencia o Solicitar Aterrizaje
1. **Selección rápida:** Puedes hacer un clic directo sobre cualquier tarjeta de avión en el radar; su código se cargará automáticamente en el selector.
2. Selecciona la prioridad en el desplegable (ej. `1 - Crítico (Mayday)` o `2 - Combustible Bajo`).
3. Haz clic en **`🚨 Insertar en Cola de Aterrizaje (Min-Heap)`**.
4. El avión se trasladará a la rampa inferior de aproximación.


<img width="1026" height="319" alt="image" src="https://github.com/user-attachments/assets/0a580239-3ced-4f54-a811-2e559e219ce0" />


---

#### Paso D: Aterrizar el Vuelo Prioritario
1. Observa la rampa inferior: el avión con mayor gravedad (ej. Nivel 1 en color rojo) se ubica en la posición `[0]` marcada con la estrella **`★ Raíz: Próximo en Aterrizar`**.
2. Haz clic en **`🛬 Aterrizar Más Urgente (O(log n))`**.
3. Aparecerá un cuadro de diálogo confirmando el aterrizaje exitoso y el avión saldrá del radar.


<img width="1022" height="167" alt="image" src="https://github.com/user-attachments/assets/c1a11e93-ab78-42ff-93e9-1b8e144101fb" />


---

#### Paso E: Deshacer Operaciones (Undo)
1. Si cometiste una equivocación o quieres demostrar cómo funciona la Pila LIFO, haz clic en **`↩ Deshacer Último Comando (Undo)`**.
2. La interfaz deshará la última acción y mostrará un mensaje confirmando la reversión del comando.


<img width="226" height="157" alt="image" src="https://github.com/user-attachments/assets/340d174e-24a2-4ed6-9835-7b5cc5a10245" />


---

## 5. Atajos de Teclado y Ayudas de Sustentación

Para una exposición académica fluida frente al docente:

| Atajo / Función | Acción Operativa | Ventaja para la Sustentación |
| :--- | :--- | :--- |
| **`F11`** | Alternar Pantalla Completa | Oculta la barra de tareas de Windows para una vista limpia tipo quiosco. |
| **`Escape`** | Salir de Pantalla Completa | Restaura la ventana maximizada con barra de título estándar. |
| **`⚡ Cargar Vuelo Demo`** | Inyección aleatoria de vuelos | Evita perder tiempo escribiendo códigos y nombres a mano con el teclado. |
| **Clic en Avión del Radar** | Selección automática en formulario | Facilita la declaración de emergencias en un solo clic. |

---

## 6. Resolución de Problemas Frecuentes

### 1. Mensaje: *"Ese vuelo no está volando"*
* **Motivo:** Se intentó solicitar aterrizaje de un vuelo que todavía está en la fila de carreteo o que no existe.
* **Solución:** Primero debes presionar **Despegar Siguiente** para que pase a estado `EN_VUELO` en el radar.

### 2. La ventana en consola se cierra inmediatamente al abrirla
* **Motivo:** Ejecutaste el archivo Python sin pasar por un entorno con la consola activa.
* **Solución:** Utiliza el lanzador directo **`Iniciar_SkyFlow_Consola.bat`**, el cual mantiene la consola abierta mediante la instrucción `pause`.

### 3. En la terminal CMD aparece *"El sistema no puede encontrar la ruta especificada"*
* **Motivo:** En CMD, el comando `cd` no cambia de unidad de disco si no se incluye el modificador `/d`.
* **Solución:** Escribe siempre `cd /d "g:\..."` con las comillas incluidas.
