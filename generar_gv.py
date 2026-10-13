import math
import os

from grafos import (
    grafo_malla,
    grafo_erdos_renyi,
    grafo_gilbert,
    grafo_geografico,
    grafo_barabasi_albert,
    grafo_dorogovtsev_mendes,
)

TAMANOS = [50, 200, 500]
DIMENSIONES_MALLA = {50: (5, 10), 200: (10, 20), 500: (20, 25)}
CARPETA_SALIDA = "gv"
MAX_INTENTOS = 1000


# Los parámetros están un poco por encima del umbral de conectividad (ln n / n)
# para que casi siempre salga conexo; si no, se vuelve a generar.
def generar_todos():
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    for n in TAMANOS:
        m = round(n * (math.log(n) + 2) / 2)
        guardar(lambda: grafo_erdos_renyi(n, m), f"1_Erdos_Rényi_n{n}")

        p = (math.log(n) + 3) / n
        guardar(lambda: grafo_gilbert(n, p), f"2_Gilbert_n{n}")

        r = math.sqrt((math.log(n) + 4) / (math.pi * n))
        guardar(lambda: grafo_geografico(n, r), f"3_Geográfico_n{n}")

        guardar(lambda: grafo_barabasi_albert(n, 4), f"4_Barabasi_albert_n{n}")

        guardar(lambda: grafo_dorogovtsev_mendes(n), f"5_Dorogovtsev_mendes_n{n}")

        filas, columnas = DIMENSIONES_MALLA[n]
        guardar(lambda: grafo_malla(filas, columnas), f"6_Malla_n{n}")


def generar_conexo(generador):
    for _ in range(MAX_INTENTOS):
        grafo = generador()
        if grafo.es_conexo():
            return grafo
    raise RuntimeError(f"No se obtuvo un grafo conexo en {MAX_INTENTOS} intentos")


def guardar(generador, nombre):
    grafo = generar_conexo(generador)
    ruta = os.path.join(CARPETA_SALIDA, f"{nombre}.gv")
    grafo.guardar_graphviz(ruta)
    print(f"{ruta}: {len(grafo.nodos)} nodos, {len(grafo.aristas)} aristas")


if __name__ == "__main__":
    generar_todos()
