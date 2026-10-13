# Clase que representa un nodo en un grafo
class Nodo:

    # Inicializa un nuevo nodo
    def __init__(self, id_nodo):
        self.id_nodo = id_nodo

    # Representación del nodo como cadena
    def __repr__(self):
        return f"Nodo({self.id_nodo!r})"

    # Compara dos nodos para igualdad
    def __eq__(self, other):
        return isinstance(other, Nodo) and self.id_nodo == other.id_nodo

    # Genera un hash del nodo basado en su identificador
    def __hash__(self):
        return hash(self.id_nodo)
