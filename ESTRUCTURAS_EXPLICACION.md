# 🧠 Justificación Teórica y Práctica de Estructuras de Datos - SkyFlow

> **Documento de Sustentación Teórica y Análisis Algorítmico**  
> **Asignatura:** Estructuras de Datos  
> **Institución:** Universidad Nacional de Colombia  

---

## 📑 Tabla de Contenidos
1. [Resumen Ejecutivo de Arquitectura](#1-resumen-ejecutivo-de-arquitectura)
2. [Tabla Comparativa de Complejidades Big-O](#2-tabla-comparativa-de-complejidades-big-o)
3. [Análisis Detallado por Estructura de Datos](#3-análisis-detallado-por-estructura-de-datos)
   - [3.1 Cola FIFO (Pista de Carreteo y Despegues)](#31-cola-fifo-pista-de-carreteo-y-despegues)
   - [3.2 Lista Doblemente Enlazada (Radar de Espacio Aéreo)](#32-lista-doblemente-enlazada-radar-de-espacio-aéreo)
   - [3.3 Min-Heap / Cola de Prioridad (Aterrizajes de Emergencia)](#33-min-heap--cola-de-prioridad-aterrizajes-de-emergencia)
   - [3.4 Pila LIFO (Historial de Torre y Función Deshacer / Undo)](#34-pila-lifo-historial-de-torre-y-función-deshacer--undo)
4. [Justificación de Optimalidad frente a Arreglos Tradicionales](#4-justificación-de-optimalidad-frente-a-arreglos-tradicionales)
5. [Diagramas de Punteros en Memoria para Sustentación](#5-diagramas-de-punteros-en-memoria-para-sustentación)

---

## 1. Resumen Ejecutivo de Arquitectura

El sistema **SkyFlow** fue diseñado para modelar un aeropuerto en tiempo real sin apoyarse en librerías ni estructuras de datos prefabricadas del lenguaje (tales como `queue.Queue`, `collections.deque` o `heapq`). Cada estructura fue programada **desde cero (from scratch)** utilizando nodos explícitos, punteros de referencia y representación binaria en arreglos base.

La arquitectura distribuye las responsabilidades en cuatro estructuras especializadas según las restricciones físicas del problema aeronáutico:

```
[AVIÓN LLEGA] ──▶ Cola FIFO (Carreteo) ──▶ Lista Doble (Radar Aéreo) ──▶ Min-Heap (Aproximación) ──▶ [PISTA]
                        ▲                               ▲                         ▲
                        └─────────────── Pila LIFO (Historial & Undo) ────────────┘
```

---

## 2. Tabla Comparativa de Complejidades Big-O

A continuación se resume el costo computacional temporal y espacial de las operaciones implementadas en SkyFlow:

| Estructura de Datos | Operación | Complejidad Temporal | Complejidad Espacial | Descripción del Movimiento de Memoria / Punteros |
| :--- | :--- | :---: | :---: | :--- |
| **Cola FIFO**<br>([cola_fifo.py](file:///g:/My%20Drive/UNAL/2026-2/Estructuras/SkyFlow/estructuras/cola_fifo.py)) | `enqueue(x)` | **$O(1)$** | $O(1)$ | Enlaza `final.siguiente = nuevo` y avanza el puntero `final`. |
| | `dequeue()` | **$O(1)$** | $O(1)$ | Lee `frente.dato` y avanza `frente = frente.siguiente`. |
| | `peek()` | **$O(1)$** | $O(1)$ | Lectura directa del dato en el puntero `frente`. |
| | `is_empty()` | **$O(1)$** | $O(1)$ | Comparación booleana `frente is None`. |
| **Lista Doble**<br>([lista_doble.py](file:///g:/My%20Drive/UNAL/2026-2/Estructuras/SkyFlow/estructuras/lista_doble.py)) | `insert(x)` | **$O(1)$** | $O(1)$ | Inserta al final: ajusta `cola.siguiente` y `nuevo.anterior`. |
| | `remove(nodo)` | **$O(1)$** | $O(1)$ | Desvincula el nodo saltando punteros anterior y siguiente. |
| | `find(codigo)` | **$O(n)$** | $O(1)$ | Recorrido secuencial desde `cabeza` hasta localizar el código. |
| **Min-Heap**<br>([cola_prioridad.py](file:///g:/My%20Drive/UNAL/2026-2/Estructuras/SkyFlow/estructuras/cola_prioridad.py)) | `insert(vuelo)` | **$O(\log n)$** | $O(1)$ | Inserta en la última posición y sube (*bubble up / shift up*). |
| | `extract_min()` | **$O(\log n)$** | $O(1)$ | Extrae la raíz `[0]`, sube el último y baja (*sift down*). |
| | `peek()` | **$O(1)$** | $O(1)$ | Acceso directo al índice `[0]` del arreglo del Heap. |
| **Pila LIFO**<br>([pila_lifo.py](file:///g:/My%20Drive/UNAL/2026-2/Estructuras/SkyFlow/estructuras/pila_lifo.py)) | `push(cmd)` | **$O(1)$** | $O(1)$ | `nuevo.siguiente = tope` y actualiza `tope = nuevo`. |
| | `pop()` | **$O(1)$** | $O(1)$ | Extrae `tope.dato` y actualiza `tope = tope.siguiente`. |
| | `peek()` | **$O(1)$** | $O(1)$ | Lectura del comando más reciente en `tope`. |

> **Costo Espacial Global:** $O(n)$, donde $n$ es el número total de aeronaves activas en el sistema, ya que cada avión ocupa exactamente un nodo o celda en su respectiva estructura sin consumo de memoria redundante.

---

## 3. Análisis Detallado por Estructura de Datos

### 3.1 Cola FIFO (Pista de Carreteo y Despegues)
* **Archivo:** `estructuras/cola_fifo.py`
* **Nodos:** `NodoCola(dato, siguiente)`
* **Punteros:** `frente` (cabeza de salida) y `final` (cola de entrada).

#### Justificación Teórica y Práctica:
En la aviación civil, los despegues convencionales se rigen bajo el principio de estricta justicia cronológica (**First-In, First-Out**). El primer avión en solicitar pista y entrar en carreteo debe ser el primero en recibir autorización de despegue.

Una Cola con punteros de `frente` y `final` garantiza que tanto la llegada de nuevos vuelos a la fila (`enqueue`) como la autorización de despegue (`dequeue`) se ejecuten en tiempo constante **$O(1)$**, sin depender del tamaño de la fila de aviones esperando pista.

---

### 3.2 Lista Doblemente Enlazada (Radar de Espacio Aéreo)
* **Archivo:** `estructuras/lista_doble.py`
* **Nodos:** `NodoDoble(dato, anterior, siguiente)`
* **Punteros:** `cabeza` (primer vuelo) y `cola` (último vuelo).

#### Justificación Teórica y Práctica:
Una vez que los aviones despegan, ingresan al espacio aéreo donde pueden volar durante lapsos indeterminados. A diferencia de una cola, **los aviones en el aire no aterrizan en el orden en que despegaron**; un avión puede aterrizar por emergencia mucho antes que otro que despegó previo a él.

Por ello, la estructura del espacio aéreo debe soportar:
1. **Inserción inmediata al despegar:** $O(1)$ al agregarse al radar.
2. **Eliminación aleatoria en tiempo constante:** Cuando un avión aterriza, se debe remover su nodo específico de la lista. En una lista doblemente enlazada, al almacenar una referencia directa al nodo (`vuelo.nodo_radar`), su desvinculación se realiza en **$O(1)$** simplemente reconectando los punteros `anterior` y `siguiente` de sus vecinos, sin necesidad de recorrer la lista.
3. **Navegabilidad bidireccional:** Permite realizar barridos del radar en ambos sentidos (de entrada o salida).

---

### 3.3 Min-Heap / Cola de Prioridad (Aterrizajes de Emergencia)
* **Archivo:** `estructuras/cola_prioridad.py`
* **Representación:** Árbol binario casi completo mapeado sobre un arreglo continuo (`datos[]`).
* **Relaciones de índices:**
  * Padre de $i$: $\lfloor(i - 1) / 2\rfloor$
  * Hijo izquierdo: $2i + 1$
  * Hijo derecho: $2i + 2$

#### Justificación Teórica y Práctica:
En una aproximación de pista, **la seguridad de la vida humana invalida el principio FIFO**. Si un avión declara emergencia médica o fallo de combustible (Nivel 1), debe tener prelación inmediata sobre vuelos regulares (Nivel 4), independientemente de cuándo haya solicitado aterrizar.

El **Min-Heap** es la estructura matemáticamente óptima para este escenario:
* Mantiene la aeronave más crítica en la raíz `[0]`, permitiendo consultar el próximo vuelo a aterrizar en **$O(1)$** con `peek()`.
* La extracción del vuelo prioritario (`extract_min`) y la inserción de nuevas emergencias (`insert`) se ejecutan en **$O(\log n)$**, reacomodando el árbol mediante intercambios locales a lo largo de la altura del árbol ($h = \lfloor\log_2 n\rfloor$).

---

### 3.4 Pila LIFO (Historial de Torre y Función Deshacer / Undo)
* **Archivo:** `estructuras/pila_lifo.py`
* **Nodos:** `NodoPila(dato, siguiente)`
* **Puntero:** `tope` (apunta al comando más reciente).

#### Justificación Teórica y Práctica:
En un centro de control operativo, los errores humanos o cambios súbitos de condiciones meteorológicas exigen reversibilidad. Para revertir un comando, este debe anularse en el orden estrictamente inverso al que ocurrió (**Last-In, First-Out**).

La Pila LIFO permite que la torre guarde una tupla `(TIPO_COMANDO, VUELO)` cada vez que ejecuta una acción. La operación `deshacer()` simplemente realiza un `pop()` en **$O(1)$** sobre el tope y ejecuta la operación inversa simétrica:
* Revertir `DESPEGAR`: Remueve el vuelo del radar en $O(1)$ y lo reinserta al frente de la cola de pista en $O(1)$.
* Revertir `ATERRIZAR`: Reinserta el vuelo en el radar y lo devuelve a la cola de aproximación.

---

## 4. Justificación de Optimalidad frente a Arreglos Tradicionales

Un evaluador en sustentación frecuentemente preguntará:  
*¿Por qué no usar simplemente una lista de Python (`list`) para todo el sistema?*

A continuación se fundamenta por qué los arreglos dinámicos tradicionales resultan ineficientes e inapropiados frente a las estructuras implementadas:

### 4.1 Ineficiencia de Arreglos en la Cola de Despegues
* **Con lista tradicional (`pop(0)`):** Al retirar el primer elemento de un arreglo contiguo en memoria, todos los $n-1$ elementos restantes deben desplazarse una posición a la izquierda para cubrir el hueco. Esto tiene una complejidad de **$O(n)$**. En un aeropuerto con cientos de vuelos en cola, cada despegue penalizaría el rendimiento del sistema.
* **Con nuestra `ColaFIFO`:** El puntero `frente` simplemente avanza una posición en memoria (`frente = frente.siguiente`). No se desplaza ningún dato, manteniendo un tiempo estricto de **$O(1)$**.

---

### 4.2 Ineficiencia de Arreglos en el Radar
* **Con lista tradicional:** Si un avión aterriza y está en el medio del arreglo, borrarlo requiere localizar su índice y desplazar el resto de elementos hacia la izquierda (**$O(n)$**).
* **Con nuestra `ListaDoble`:** Al guardar `nodo_radar` en la entidad `Vuelo`, conocemos la dirección de memoria exacta del nodo. Desvincularlo es una operación puramente local que toma **$O(1)$** sin importar si en el radar hay 10 o 100,000 aviones.

---

### 4.3 Ineficiencia de Arreglos en la Cola de Prioridad
* **Opción A (Arreglo desordenado):** Insertar es $O(1)$, pero para encontrar el vuelo de mayor emergencia y aterrizarlo se debe recorrer todo el arreglo para buscar el mínimo, tomando **$O(n)$**.
* **Opción B (Arreglo ordenado):** Encontrar y extraer el mínimo es $O(1)$, pero insertar una nueva aeronave requiere desplazar elementos para mantener el orden, tomando **$O(n)$**.
* **Con nuestro `Min-Heap`:** No se incurre en el costo $O(n)$ de ninguna de las opciones anteriores; tanto la inserción como la extracción se equilibran en **$O(\log n)$**, lo cual es logarítmico y prácticamente instantáneo en tiempo real.

---

## 5. Diagramas de Punteros en Memoria para Sustentación

Estos esquemas ASCII ilustran con precisión qué referencias se mueven en memoria durante cada operación:

### 5.1 Encolamiento y Desencolamiento en `ColaFIFO`
```text
ENQUEUE (Llega LA202):
1. Crear nuevo nodo: [LA202 | •→None]
2. final.siguiente = nuevo
3. final = nuevo

frente                                  final
  ▼                                       ▼
[AV101 | •] ──────────▶ [IB602 | •] ──────────▶ [LA202 | •→None]

DEQUEUE (Despega AV101):
1. dato = frente.dato
2. frente = frente.siguiente

(AV101 liberado)        frente                  final
                          ▼                       ▼
                        [IB602 | •] ──────────▶ [LA202 | •→None]
```

---

### 5.2 Eliminación en `ListaDoble` (Aterriza un vuelo del medio)
```text
Nodo objetivo: [V2]

Antes:
[V1] ◀──────────────▶ [V2] ◀──────────────▶ [V3]
  │                      │                     │
  └─ anterior.siguiente ─┴─ siguiente.anterior ┘

Reconexión de punteros en O(1):
V2.anterior.siguiente = V2.siguiente  (V1 apunta directo a V3)
V2.siguiente.anterior = V2.anterior  (V3 apunta directo a V1)

Después:
[V1] ◀──────────────────────────────────────▶ [V3]
```

---

### 5.3 Inserción y Flotación en `Min-Heap`
```text
Llega emergencia Nivel 1 a un Heap que tiene elementos [2, 3, 4]:

Paso 1: Se inserta al final del arreglo
Índice:     0    1    2    3
Valor:     [2]  [3]  [4]  [1]   (1 está en posición 3, padre en índice 1 que vale 3)

Paso 2: Subir / Bubble Up (1 es menor que 3, se intercambian)
Índice:     0    1    2    3
Valor:     [2]  [1]  [4]  [3]   (1 está en posición 1, padre en índice 0 que vale 2)

Paso 3: Subir / Bubble Up (1 es menor que 2, se intercambian)
Índice:     0    1    2    3
Valor:     [1]  [2]  [4]  [3]   (1 llegó a la raíz: O(log n))
```

---

## 6. Conclusión Teórica

La combinación de estas cuatro estructuras de datos demuestra que **no existe una única estructura universal para todos los problemas**. Cada componente del aeropuerto tiene invariantes y restricciones operativas distintas que solo pueden resolverse de manera óptima ($O(1)$ y $O(\log n)$) cuando se selecciona la estructura de datos que modela naturalmente la relación entre los datos y el tiempo.
