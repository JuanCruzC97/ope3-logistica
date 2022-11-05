class Camion(object):
    """ 
    La clase Camión permite generar instancias de camiones con sus respectivas características:
        - ix: Identificador del camión.
        - carga_max: Máxima carga admitida.
        - pedidos_max: Máximo número de pedidos admitidos.
        - dist_max: Máxima distancia entre clientes.
        
    Dentro de pedidos_asignados se guardan todos los pedidos que se agregan al camión acompañados del ix del pedido.
    Se puede acceder fácilmente a la carga total actual del camion y cantidad de pedidos con esos atributos.
    """
    
    def __init__(self, ix, carga_max, pedidos_max, dist_max):
        self.ix = ix
        self.carga_max = carga_max
        self.pedidos_max = pedidos_max
        self.dist_max = dist_max
        self.pedidos_asignados = {}
        self.carga_total = 0
        self.cantidad_pedidos = 0
        
        
    def __str__(self):
        return f'Camión {self.ix}\nCarga Total {self.carga_total} tn\nPedidos {[ped.ix for ped in self.pedidos_asignados.values()]}\nCosto Total {self.get_costo()}\nCosto por tn {self.get_costo_tn()}'
    
    def __repr__(self):
        return f'Camión {self.ix}\nCarga Total {self.carga_total} tn\nPedidos {[ped.ix for ped in self.pedidos_asignados.values()]}\nCosto Total {self.get_costo()}\nCosto por tn {self.get_costo_tn()}'
        
    def get_ix(self):
        """
        Returns:
            int or str: Identificador ix del camión.
        """
        return self.ix
    
    def get_carga_total(self):
        """
        Returns:
            int: Carga total de pedidos asignados del camión.
        """       
        return self.carga_total
    
    def count_pedidos(self):
        """
        Returns:
            int: Cantidad de pedidos asignados del camión.
        """          
        return self.cantidad_pedidos
        
    def get_ix_pedidos(self):
        """
        Returns:
            list: Lista de ix de pedidos asignados al camión.
        """        
        return list(self.pedidos_asignados.keys())
    
    def get_pedidos(self):
        """
        Returns:
            list: Lista de pedidos asignados al camión.
        """     
        return list(self.pedidos_asignados.values())
    
    def get_pedido(self, ix):
        """
        Args:
            ix (int or str): Código identificador del pedido que queremos obtener de los pedidos asignados al camión.

        Returns:
            Pedido: Pedido ix asignado al camión.
        """
        return self.pedidos_asignados.get(ix)    
    
    def _check_pedido_carga(self, pedido):
        """ 
        Permite pasarle al camión un nuevo pedido y revisar carga máxima.
            - Devuelve True si sumando el nuevo pedido no excedemos la carga máxima.
            - Devuelve False si sumando el nuevo pedido excedemos la carga máxima.
        """
        return (self.carga_total + pedido.carga) <= self.carga_max
    
    def _check_pedido_cantidad(self):
        """ 
        Permite revisar si se alcanzó la cantidad de pedidos máxima.
            - Devuelve True si sumando el nuevo pedido no excedemos la cantidad de pedidos máxima.
            - Devuelve False si sumando el nuevo pedido excedemos la cantidad de pedidos máxima.
        """
        return self.cantidad_pedidos < self.pedidos_max
    
    def _check_pedido_distancia(self, pedido):
        """ 
        Permite pasarle al camión un nuevo pedido y revisar que su distancia no supere la distancia máxima
        con el resto de pedidos.
            - Devuelve True si sumando el nuevo pedido no excedemos la distancia máxima para ningún pedido.
            - Devuelve False si sumando el nuevo pedido excedemos la distancia máxima en al menos un pedido.
        """
        dist_check = [pedido.distancia(other) <= self.dist_max for other in self.get_pedidos()]
        return all(dist_check)
    
    def check_nuevo_pedido(self, pedido):
        """ 
        Permite pasarle al camión un nuevo pedido y revisar si puede agregarse al camión cumpliendo
        la carga máxima, distancia máxima y cantidad de pedidos máxima.
            - Devuelve True si sumando el nuevo pedido no excedemos ninguna restricción.
            - Devuelve False si sumando el nuevo pedido excedemos alguna restricción.
        """
        #return not pedido.asignado and self._check_pedido_carga(pedido) and self._check_pedido_cantidad(pedido) and self._check_pedido_distancia(pedido)
        return self._check_pedido_carga(pedido) and self._check_pedido_cantidad() and self._check_pedido_distancia(pedido)
        
    def check_intercambio_pedido(self, pedido):
        """ 
        Permite pasarle al camión un pedido que no pertenezca al mismo y revisar a 
        que pedidos ya asignados podría reemplazar. Esta comparación se realiza con el pedido que se pasa al método
        contra todos los pedidos asignados en el camión.
            
        Que un nuevo pedido pueda reemplazar a otro implica que:
            - Eliminando la carga del pedido original (a reemplazar) y agregando la nueva carga no se supera la carga máxima.
            - La distancia del nuevo pedido con los pedidos restantes del camión (sin tener en cuenta el pedido a reemplazar) no supera la distancia máxima.
            
        Returns:
            list: Lista de ix de pedidos que podrían ser reemplazados por el pedido pasado como argumento del método.
        """    
        
        # Revisamos que el pedido no esté asignado previamente al camión.
        if pedido.ix not in self.get_ix_pedidos():
            
            # Creamos una lista de ixs reemplazables por el pedido nuevo.
            ix_pedidos_reemplazables = []
            
            # Para cada uno de los pedidos ya asignado al camión se hace el chequeo.
            for pedido_original in self.get_pedidos():
                # Calculamos la carga nueva que tendría el camión con el reemplazo de pedidos.
                nueva_carga = self.carga_total + pedido.carga - pedido_original.carga
                # Generamos una lista de bool revisando si el nuevo pedido incorporado supera la distancia máxima con los pedidos restantes en el camión.
                distancias = [pedido.distancia(pedido_restante) <= self.dist_max for pedido_restante in self.get_pedidos() if pedido_restante.ix != pedido_original.ix]
                
                # Si la nueva carga no supera la carga máxima y las distancias con pedidos restantes son todas menores al máximo
                # agregamos el ix del pedido a reemplazar en la lista.
                if nueva_carga <= self.carga_max and all(distancias):
                    ix_pedidos_reemplazables.append(pedido_original.ix)
                    
            return ix_pedidos_reemplazables
        
        # Si el pedido ya estaba asignado al camión se devuelve una lista vacía.
        else:
            return []
        
        
    def add_pedido(self, pedido):
        """
        Permite pasarle al camión un pedido no asignado previamente e incorporarlo al mismo.
        Este método no realiza los chequeos de las restricciones del camión.
        """
        if not pedido.asignado:
            # Se agrega el pedido al diccionario de pedidos asignados de este camión.
            self.pedidos_asignados[pedido.ix] = pedido
            # Se actualiza la carga total y cantidad de pedidos totales.
            self.carga_total += pedido.carga
            self.cantidad_pedidos += 1
            # Se actualizan las propiedades del pedido agregado.
            pedido.asignado = True
            pedido.camion_ix = self.ix
        #     return True
        # else:
        #     return False
            
    def add_pedido_checked(self, pedido):
        """
        Permite pasarle al camión un pedido no asignado previamente e incorporarlo al mismo.
        A diferencia del método add_pedido() este método sólo agrega el pedido si pasa los chequeos de las restricciones.
        """
        if self.check_nuevo_pedido(pedido):
            self.add_pedido(pedido)
        
    
    def remove_pedido(self, pedido_ix):
        """
        Permite pasarle al camión un ix de un pedido asignado y eliminarlo del diccionario
        de pedidos asignados.
        """
        # Confirma que el pedido esté asignado a este camión.
        if pedido_ix in self.get_ix_pedidos():
            # Actualiza los parámetros del pedido.
            self.get_pedido(pedido_ix).asignado = False
            self.get_pedido(pedido_ix).camion_ix = None
            # Actualiza los parámetros del camión.
            self.carga_total -= self.pedidos_asignados.get(pedido_ix).carga
            self.cantidad_pedidos -= 1
            # Elimina el pedido.
            self.pedidos_asignados.pop(pedido_ix)
        else:
            print(f"El pedido {pedido_ix} no está en el camión {self.ix}")    

    
    def get_costo(self):
        """
        Returns:
            int: Costo del camión en función de la carga total.
        """   
         
        if self.carga_total == 0:
            costo = 5000
        elif self.carga_total <= 4:
            costo = 5600
        elif self.carga_total > 4 and self.carga_total < 6.5:
            costo = 1400*self.carga_total
        elif self.carga_total >= 6.5 and self.carga_total < 9.5:
            costo = 1200*self.carga_total
        else:
            costo = 1000*self.carga_total
                
        return costo 
    
    def get_costo_tn(self):
        """
        Returns:
            float: Costo por tn del camión en función de la carga total.
        """   
        if self.carga_total != 0:
            return self.get_costo()/self.carga_total
        else:
            return None

    def reset_pedidos(self):
        """
        Elimina todos los pedidos asignados del camión.
        """
        self.pedidos_asignados.clear()
        self.carga_total = 0
        self.cantidad_pedidos = 0
        
        
        
        
        
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
    
    