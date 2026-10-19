# Genera las imágenes PNG de los grafos generados y de los árboles calculados
# a partir de los archivos .gv, usando Graphviz (https://graphviz.org).
import os
import shutil
import subprocess

CARPETAS = {
    os.path.join("gv", "generados"): os.path.join("imagenes", "generados"),
    os.path.join("gv", "calculados"): os.path.join("imagenes", "calculados"),
}
RUTA_GRAPHVIZ_WINDOWS = r"C:\Program Files\Graphviz\bin"


# Busca un programa de Graphviz en el PATH o en la ruta de instalación de Windows
def programa_graphviz(nombre):
    ruta = shutil.which(nombre)
    if ruta is None:
        ruta = shutil.which(nombre, path=RUTA_GRAPHVIZ_WINDOWS)
    if ruta is None:
        raise RuntimeError(f"No se encontró '{nombre}'; instala Graphviz y agrégalo al PATH")
    return ruta


# Elige el algoritmo de dibujo según el tipo de grafo:
# - malla y sus árboles: neato, con cada nodo fijo en su posición de la cuadrícula
# - árboles BFS: twopi, que coloca la raíz al centro y cada capa en un anillo
# - árboles DFS y demás grafos: sfdp, pensado para grafos grandes
def elegir_layout(nombre):
    if "Malla" in nombre:
        return "neato"
    if "_BFS" in nombre:
        return "twopi"
    return "sfdp"


# Devuelve los identificadores de los nodos tal como aparecen en el .gv (con comillas)
def leer_nodos(texto):
    return [l.strip()[:-1] for l in texto.splitlines()[1:]
            if l.strip().endswith(";") and "--" not in l and "->" not in l]


# Agrega estilo al texto .gv sin modificar el archivo original:
# nodos como puntos (con etiqueta solo en grafos pequeños) y la raíz en rojo.
# En la malla, el nodo "(i, j)" se fija en la fila i y la columna j.
def dar_estilo(texto, nombre):
    lineas = texto.splitlines()
    nodos = leer_nodos(texto)

    if len(nodos) <= 30:
        estilo_nodo = 'node [shape=circle, fontsize=9, width=0.45, fixedsize=true, style=filled, fillcolor="#dbe9f6"];'
    else:
        estilo_nodo = 'node [shape=point, width=0.08, color="#1f4e79"];'
    estilo = [
        'graph [overlap=false, splines=false, outputorder=edgesfirst, size="10,10", dpi=100, bgcolor=white];',
        estilo_nodo,
        'edge [color="#7f7f7f", penwidth=0.8];',
    ]
    if "Malla" in nombre:
        separacion = 0.8
        for nodo in nodos:
            i, j = (int(x) for x in nodo.strip('"()').split(","))
            estilo.append(f'{nodo} [pos="{j * separacion},{-i * separacion}!"];')
    if nodos:
        tamano = "" if len(nodos) <= 30 else ", width=0.2"
        estilo.append(f'{nodos[0]} [root=true, color=red, fillcolor=red, style=filled{tamano}];')
    return "\n".join([lineas[0]] + estilo + lineas[1:]) + "\n"


def dibujar(ruta_gv, ruta_png):
    nombre = os.path.basename(ruta_gv)
    with open(ruta_gv) as f:
        texto = f.read()
    comando = [programa_graphviz(elegir_layout(nombre)), "-Tpng", "-o", ruta_png]
    subprocess.run(comando, input=dar_estilo(texto, nombre).encode("utf-8"), check=True)
    print(ruta_png)


def generar_todas():
    for carpeta_gv, carpeta_png in CARPETAS.items():
        os.makedirs(carpeta_png, exist_ok=True)
        for archivo in sorted(os.listdir(carpeta_gv)):
            if archivo.endswith(".gv"):
                dibujar(os.path.join(carpeta_gv, archivo),
                        os.path.join(carpeta_png, archivo[:-3] + ".png"))


if __name__ == "__main__":
    generar_todas()
