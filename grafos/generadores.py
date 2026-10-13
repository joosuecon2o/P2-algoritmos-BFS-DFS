# librería de generación y manejo de grafos
import math
import random

# Importa la clase Grafo desde su módulo.
from .grafo import Grafo

# Generadores de grafos específicos
def grafo_malla(m, n, dirigido=False): # grafo de tipo malla
    """
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    grafo = Grafo(dirigido)
    for i in range(m):
        for j in range(n):
            grafo.agregar_nodo((i, j))
    for i in range(m):
        for j in range(n):
            if i < m - 1:
                grafo.agregar_arista((i, j), (i + 1, j))
            if j < n - 1:
                grafo.agregar_arista((i, j), (i, j + 1))
    return grafo

# Generador de grafo aleatorio con el modelo Erdos-Renyi
def grafo_erdos_renyi(n, m, dirigido=False): # grafo aleatorio Erdos-Renyi
    """
    Genera grafo aleatorio con el modelo Erdos-Renyi
    :param n: número de nodos (> 0)
    :param m: número de aristas (>= n-1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    max_m = n * (n - 1) if dirigido else n * (n - 1) // 2
    if m > max_m:
        raise ValueError(f"m={m} excede el máximo de aristas posibles ({max_m}) para n={n}")

    grafo = Grafo(dirigido)
    for i in range(n):
        grafo.agregar_nodo(i)

    aristas_creadas = 0
    while aristas_creadas < m:
        u, v = random.sample(range(n), 2)
        if grafo.agregar_arista(u, v) is not None:
            aristas_creadas += 1
    return grafo

# Generador de grafo aleatorio con el modelo Gilbert
def grafo_gilbert(n, p, dirigido=False): # grafo aleatorio Gilbert
    """
    Genera grafo aleatorio con el modelo Gilbert
    :param n: número de nodos (> 0)
    :param p: probabilidad de crear una arista (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    grafo = Grafo(dirigido)
    for i in range(n):
        grafo.agregar_nodo(i)

    for i in range(n):
        for j in range(n):
            if i == j or (not dirigido and j < i):
                continue
            if random.random() < p:
                grafo.agregar_arista(i, j)
    return grafo

# Generador de grafo aleatorio con el modelo geográfico simple
def grafo_geografico(n, r, dirigido=False): # grafo aleatorio geográfico simple
    """
    Genera grafo aleatorio con el modelo geográfico simple
    :param n: número de nodos (> 0)
    :param r: distancia máxima para crear un nodo (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    grafo = Grafo(dirigido)
    posiciones = [(random.random(), random.random()) for _ in range(n)]
    for i in range(n):
        grafo.agregar_nodo(i)

    for i in range(n):
        for j in range(n):
            if i == j or (not dirigido and j < i):
                continue
            dx = posiciones[i][0] - posiciones[j][0]
            dy = posiciones[i][1] - posiciones[j][1]
            if math.hypot(dx, dy) <= r:
                grafo.agregar_arista(i, j)
    return grafo

# Generador de grafo aleatorio con el modelo Barabasi-Albert
def grafo_barabasi_albert(n, d, dirigido=False): # grafo aleatorio Barabasi-Albert
    """
    Genera grafo aleatorio con la variante del modelo Barabasi-Albert:
    cada nodo nuevo se conecta a un nodo existente v con probabilidad
    1 - grado(v) / d, así que ningún nodo pasa de d aristas.
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    grafo = Grafo(dirigido)
    for i in range(min(d, n)):
        grafo.agregar_nodo(i)
    for i in range(min(d, n)):
        for j in range(i + 1, min(d, n)):
            grafo.agregar_arista(i, j)

    for nuevo in range(d, n):
        grafo.agregar_nodo(nuevo)
        candidatos = list(range(nuevo))
        random.shuffle(candidatos)
        for objetivo in candidatos:
            if grafo.grado(nuevo) >= d:
                break
            probabilidad = 1 - grafo.grado(objetivo) / d
            if random.random() < probabilidad:
                grafo.agregar_arista(nuevo, objetivo)
    return grafo

# Generador de grafo aleatorio con el modelo Dorogovtsev-Mendes
def grafo_dorogovtsev_mendes(n, dirigido=False): # grafo aleatorio Dorogovtsev-Mendes
    """
    Genera grafo aleatorio con el modelo Dorogovtsev-Mendes
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    grafo = Grafo(dirigido)
    for i in range(3):
        grafo.agregar_nodo(i)
    grafo.agregar_arista(0, 1)
    grafo.agregar_arista(1, 2)
    grafo.agregar_arista(2, 0)

    for nuevo in range(3, n):
        grafo.agregar_nodo(nuevo)
        arista = random.choice(grafo.aristas)
        grafo.agregar_arista(nuevo, arista.origen.id_nodo)
        grafo.agregar_arista(nuevo, arista.destino.id_nodo)
    return grafo
