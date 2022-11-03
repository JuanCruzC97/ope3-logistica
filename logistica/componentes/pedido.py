
class Pedido(object):
    """ 
    La clase Pedido permite generar instancias de pedidos de clientes con sus respectivas características:
        - ix: Identificador del pedido.
        - x: Coordenada x de localización.
        - y: Coordenada y de localización.
        - carga: Carga del pedido.
        
    Si el pedido está asignado dicho parámetro toma valor True. El parámetro camion_ix indica el ix del camión al 
    que el pedido está asignado.
    """
    
    def __init__(self, ix, x, y, carga):
        self.ix = ix
        self.x = x
        self.y = y
        self.carga = carga
        self.asignado = False
        self.camion_ix = None
        
    def __str__(self):
        return f'Pedido {self.ix}\nCarga {self.carga} tn\nAsignado {self.asignado}\nAsignado a Camion {self.camion_ix}'
    
    def __repr__(self):
        return f'Pedido {self.ix}\nCarga {self.carga} tn\nAsignado {self.asignado}\nAsignado a Camion {self.camion_ix}'
    
    def get_ix(self):
        """
        Returns:
            int or str: Identificador ix del pedido.
        """
        return self.ix
    
    def get_carga(self):
        """
        Returns:
            float: Carga del pedido.
        """
        return self.carga
    
    def distancia(self, other):
        """Calcula la distancia entre la instancia del pedido y un segundo pedido pasado como argumento other.

        Args:
            other (Pedido): Pedido con el que queremos obtener la distancia respecto de la instancia actual.

        Returns:
            float: Distancia entre la instancia del pedido y el pedido en el argumento del método.
        """
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**(1/2)
        return round(dist, 1)
    
    