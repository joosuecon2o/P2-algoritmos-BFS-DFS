# Algoritmos BFS y DFS

Proyecto 2 de Diseño y Análisis de Algoritmos: a partir de la biblioteca de grafos del [Proyecto 1](https://github.com/joosuecon2o/P1-biblioteca-grafos), se implementan los algoritmos BFS y DFS (recursivo e iterativo). Dado un nodo fuente `s`, cada uno calcula el árbol inducido por el recorrido.

## Métodos nuevos de la clase `Grafo`

Los tres métodos están en `grafos/grafo.py`. Cada uno recibe el identificador del nodo fuente y devuelve el árbol como un nuevo objeto `Grafo`, que contiene los nodos alcanzables desde `s` y las aristas (padre, hijo) del recorrido.

| Método | Algoritmo | Funcionamiento |
|---|---|---|
| `BFS(self, s)` | Búsqueda a lo ancho | Explora por capas: `L[0] = {s}` y `L[i+1]` contiene los nodos no descubiertos con una arista hacia `L[i]`. Cada nodo se une con el nodo de la capa anterior que lo descubrió. |
| `DFS_R(self, s)` | Búsqueda en profundidad, recursiva | `DFS(u)` marca `u` como explorado y, por cada arista `(u, v)` con `v` no explorado, agrega `(u, v)` al árbol e invoca `DFS(v)`. |
| `DFS_I(self, s)` | Búsqueda en profundidad, iterativa | Sustituye la recursión por una pila explícita de pares (nodo, vecinos pendientes), que reproduce la pila de llamadas de `DFS_R`. |

Todos son O(n + m). Como `DFS_I` simula exactamente la recursión de `DFS_R`, ambos producen el mismo árbol a partir del mismo nodo fuente. `DFS_R` aumenta temporalmente el límite de recursión de Python para no fallar en grafos con caminos largos. Aun así, la pila del sistema impone un tope: en Python 3.6 sobre Windows, `DFS_R` funciona hasta unos 4000 niveles de profundidad. Para grafos más profundos conviene usar `DFS_I`, que no tiene ese límite. Los árboles de este proyecto llegan a lo más a 417 niveles.

El código está probado con Python 3.6.8, la versión que pide el curso.

## Estructura

- `grafos/` — código fuente de la biblioteca
  - `nodo.py` — clase `Nodo`
  - `arista.py` — clase `Arista`
  - `grafo.py` — clase `Grafo`, con `BFS`, `DFS_R` y `DFS_I`
  - `generadores.py` — generadores de grafos (malla, Erdős–Rényi, Gilbert, geográfico simple, Barabási–Albert y Dorogovtsev–Mendes)
- `generar_gv.py` — genera los grafos y calcula sus árboles
- `generar_imagenes.py` — dibuja todos los `.gv` con Graphviz
- `gv/generados/` — 18 grafos generados: 6 modelos × 30, 100 y 500 nodos
- `gv/calculados/` — 54 árboles: BFS, DFS_R y DFS_I de cada grafo generado
- `imagenes/generados/` y `imagenes/calculados/` — una imagen PNG por cada archivo `.gv`

Los nombres de los árboles indican el grafo de origen y el algoritmo, por ejemplo `3_Geografico_n100_DFS_I.gv`.

## Uso

```python
from grafos import grafo_gilbert

g = grafo_gilbert(30, 0.2)

arbol_bfs = g.BFS(0)
arbol_dfs_r = g.DFS_R(0)
arbol_dfs_i = g.DFS_I(0)

print(arbol_bfs)        # Grafo(nodos=..., aristas=..., dirigido=False)
arbol_bfs.guardar_graphviz("bfs.gv")
```

## Generar los archivos

```
python generar_gv.py
python generar_imagenes.py
```

`generar_gv.py` vuelve a generar cada grafo hasta obtener uno conexo, de modo que los árboles abarcan todos los nodos. El nodo fuente es el primero del grafo: `0` en los modelos aleatorios y `(0, 0)` en la malla.

`generar_imagenes.py` requiere [Graphviz](https://graphviz.org). En las imágenes, el nodo fuente aparece en rojo, y la forma de dibujo depende del grafo:

- **Árboles BFS:** se dibujan con `twopi`, que coloca la raíz al centro y cada capa en un anillo.
- **Malla y sus árboles:** se dibujan con `neato`, con cada nodo en su posición de la cuadrícula.
- **Demás grafos y árboles DFS:** se dibujan con `sfdp`.
