# Módulo de grafos que contiene las clases Nodo, Arista y Grafo, así como funciones para generar grafos específicos.
# Importa las clases Nodo, Arista y Grafo desde sus respectivos módulos.
from .nodo import Nodo
from .arista import Arista

# Importa la clase Grafo desde su módulo.
class Grafo:

    # Inicializa un nuevo grafo
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.nodos = {}
        self.aristas = []
        self._vecinos = {}
        self._grado = {}

    # Agrega un nodo al grafo
    def agregar_nodo(self, id_nodo):
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = Nodo(id_nodo)
            self._vecinos[id_nodo] = set()
            self._grado[id_nodo] = 0
        return self.nodos[id_nodo]

    # Verifica si existe una arista entre dos nodos
    def existe_arista(self, id_nodo1, id_nodo2):
        return id_nodo2 in self._vecinos.get(id_nodo1, ())

    # Agrega una arista entre dos nodos
    def agregar_arista(self, id_nodo1, id_nodo2, peso=None):
        self.agregar_nodo(id_nodo1)
        self.agregar_nodo(id_nodo2)
        if id_nodo1 == id_nodo2 or self.existe_arista(id_nodo1, id_nodo2):
            return None
        arista = Arista(self.nodos[id_nodo1], self.nodos[id_nodo2], self.dirigido, peso)
        self.aristas.append(arista)
        self._vecinos[id_nodo1].add(id_nodo2)
        if not self.dirigido:
            self._vecinos[id_nodo2].add(id_nodo1)
        self._grado[id_nodo1] += 1
        self._grado[id_nodo2] += 1
        return arista

    # Obtiene los vecinos de un nodo
    def vecinos(self, id_nodo):
        return self._vecinos.get(id_nodo, set())
    def grado(self, id_nodo):
        return self._grado[id_nodo]

    # Verifica si todos los nodos están conectados (sin nodos aislados ni componentes sueltas)
    def es_conexo(self):
        if not self.nodos:
            return True
        vecinos_sin_direccion = {id_nodo: set() for id_nodo in self.nodos}
        for arista in self.aristas:
            vecinos_sin_direccion[arista.origen.id_nodo].add(arista.destino.id_nodo)
            vecinos_sin_direccion[arista.destino.id_nodo].add(arista.origen.id_nodo)
        inicio = next(iter(self.nodos))
        visitados = {inicio}
        pila = [inicio]
        while pila:
            actual = pila.pop()
            for vecino in vecinos_sin_direccion[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    pila.append(vecino)
        return len(visitados) == len(self.nodos)

    # Guarda el grafo en un archivo en formato Graphviz
    def guardar_graphviz(self, archivo):
        conector = "->" if self.dirigido else "--"
        tipo = "digraph" if self.dirigido else "graph"
        with open(archivo, "w") as f:
            f.write(f"{tipo} G {{\n")
            for id_nodo in self.nodos:
                f.write(f'    "{id_nodo}";\n')
            for arista in self.aristas:
                f.write(f'    "{arista.origen.id_nodo}" {conector} "{arista.destino.id_nodo}";\n')
            f.write("}\n")

    # Devuelve el número de nodos en el grafo
    def __len__(self):
        return len(self.nodos)

    # Representación del grafo como cadena
    def __repr__(self):
        return f"Grafo(nodos={len(self.nodos)}, aristas={len(self.aristas)}, dirigido={self.dirigido})"
