# Biblioteca de generación y manejo de grafos

Proyecto 1 de Diseño y Análisis de Algoritmos: biblioteca orientada a objetos en Python 3 para describir y utilizar grafos.

## Estructura

- `grafos/` — código fuente de la biblioteca
  - `nodo.py` — clase `Nodo`
  - `arista.py` — clase `Arista`
  - `grafo.py` — clase `Grafo` (incluye `guardar_graphviz` para exportar a formato GraphViz)
  - `generadores.py` — funciones para generar grafos
- `generar_gv.py` — script que genera los 18 archivos `.gv` (3 tamaños de 50, 200 y 500 nodos por cada uno de los 6 modelos)
- `gv/` — archivos `.gv` generados
- `imagenes/` — imágenes de los grafos generados (creadas con Gephi)
- `reporte.tex` — reporte del proyecto en LaTeX
- `reporte.pdf` — reporte compilado

## Representación

La clase `Grafo` usa una lista de adyacencia basada en conjuntos, junto con una lista de aristas:

| Atributo | Tipo | Contenido |
|---|---|---|
| `nodos` | `dict` | identificador → objeto `Nodo` |
| `aristas` | `list` | objetos `Arista`, en orden de inserción |
| `_vecinos` | `dict` de `set` | identificador → identificadores adyacentes |
| `_grado` | `dict` | identificador → número de aristas incidentes |

Los grafos son simples: `agregar_arista` ignora los lazos y las aristas repetidas, y en esos casos devuelve `None`.

## Generadores

Todos reciben el parámetro opcional `dirigido` (por omisión `False`) y devuelven un `Grafo`.

| Función | Modelo | Parámetros |
|---|---|---|
| `grafo_malla(m, n)` | Malla | `m` columnas y `n` filas |
| `grafo_erdos_renyi(n, m)` | Erdős–Rényi | `n` nodos y `m` aristas elegidas al azar |
| `grafo_gilbert(n, p)` | Gilbert | `n` nodos; cada arista se crea con probabilidad `p` |
| `grafo_geografico(n, r)` | Geográfico simple | `n` nodos en el cuadrado unitario; se conectan los que están a distancia ≤ `r` |
| `grafo_barabasi_albert(n, d)` | Barabási–Albert | `n` nodos con grado máximo `d` |
| `grafo_dorogovtsev_mendes(n)` | Dorogovtsev–Mendes | `n` nodos; cada nodo nuevo se une a los extremos de una arista al azar |

Los modelos aleatorios usan el módulo `random` sin fijar semilla, así que cada ejecución produce un grafo distinto. Para obtener resultados reproducibles, llama a `random.seed(...)` antes de generar.

## Uso

```python
from grafos import grafo_gilbert

g = grafo_gilbert(50, 0.1)

print(g)                # Grafo(nodos=50, aristas=..., dirigido=False)
print(g.grado(0))       # grado del nodo 0
print(g.vecinos(0))     # conjunto de vecinos del nodo 0
print(g.es_conexo())    # True si todos los nodos están conectados

g.guardar_graphviz("mi_grafo.gv")
```

## Generar los archivos .gv

```
python generar_gv.py
```

El script vuelve a generar cada grafo hasta obtener uno conexo y lo guarda en `gv/`. Las imágenes de `imagenes/` no se generan con el script: se hicieron a mano en Gephi a partir de esos archivos.

## Reporte

`reporte.tex` describe el funcionamiento de las clases y de los generadores, e incluye las 18 imágenes. Para compilarlo se necesita una distribución de LaTeX (por ejemplo, MiKTeX) y ejecutar dos veces, para que se resuelvan el índice y las referencias:

```
pdflatex reporte.tex
pdflatex reporte.tex
```

El reporte carga las imágenes desde `imagenes/`, así que debe compilarse desde la raíz del proyecto.
