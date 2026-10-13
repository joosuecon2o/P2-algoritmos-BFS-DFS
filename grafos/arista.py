# Clase que representa una arista en un grafo

class Arista:
    # Inicializa una nueva arista
    def __init__(self, origen, destino, dirigida=False, peso=None):
        self.origen = origen
        self.destino = destino
        self.dirigida = dirigida
        self.peso = peso

    # Representación de la arista como cadena
    def __repr__(self):
        conector = "->" if self.dirigida else "--"
        return f"Arista({self.origen.id_nodo!r} {conector} {self.destino.id_nodo!r})"
