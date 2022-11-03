class Camion(object):
    """ La clase Camión permite generar instancias de camiones con sus respectivas características:
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
    
    def _check_pedido_carga(self, pedido):
        """ Este método del camión permite pasarle al camión un nuevo pedido y revisar carga máxima.
            - Devuelve True si sumando el nuevo pedido no excedemos la carga máxima.
            - Devuelve False si sumando el nuevo pedido excedemos la carga máxima.
        """
        return (self.carga_total + pedido.carga) <= self.carga_max
    
    def _check_pedido_cantidad(self):
        """ Este método del camión permite pasarle al camión un nuevo pedido y revisar cantidad de pedidos máxima.
            - Devuelve True si sumando el nuevo pedido no excedemos la cantidad de pedidos máxima.
            - Devuelve False si sumando el nuevo pedido excedemos la cantidad de pedidos máxima.
        """
        return self.cantidad_pedidos < self.pedidos_max
    
    def _check_pedido_distancia(self, pedido):
        """ Este método del camión permite pasarle al camión un nuevo pedido y revisar que su distancia no supere la distancia máxima
            con el resto de pedidos.
            - Devuelve True si sumando el nuevo pedido no excedemos la distancia máxima para ningún pedido.
            - Devuelve False si sumando el nuevo pedido excedemos la distancia máxima en al menos un pedido.
        """
        dist_check = [pedido.distancia(other) <= self.dist_max for other in self.pedidos_asignados.values()]
        return all(dist_check)
    
    def check_nuevo_pedido(self, pedido):
        #return not pedido.asignado and self._check_pedido_carga(pedido) and self._check_pedido_cantidad(pedido) and self._check_pedido_distancia(pedido)
        return self._check_pedido_carga(pedido) and self._check_pedido_cantidad() and self._check_pedido_distancia(pedido)
        
    def check_intercambio_pedido(self, pedido):
        ix_pedidos_intercambio = []
        
        for pedido_original in self.pedidos_asignados.values():
            
            nueva_carga = self.carga_total + pedido.carga - pedido_original.carga
            distancias = [pedido.distancia(pedido_restante) <= self.dist_max for pedido_restante in self.pedidos_asignados.values() if pedido_restante.ix != pedido_original.ix]
            
            if nueva_carga <= self.carga_max and all(distancias):
                
                ix_pedidos_intercambio.append(pedido_original.ix)
                
        return ix_pedidos_intercambio
                
        
        
    def add_pedido(self, pedido):
        if not pedido.asignado:
            self.pedidos_asignados[pedido.ix] = pedido
            self.carga_total += pedido.carga
            self.cantidad_pedidos += 1
            pedido.asignado = True
            pedido.camion_ix = self.ix
        #     return True
        # else:
        #     return False
            
    def add_pedido_checked(self, pedido):
        if self.check_nuevo_pedido(pedido):
            self.add_pedido(pedido)
        
    
    def remove_pedido(self, pedido_ix):
        self.pedidos_asignados.get(pedido_ix).asignado = False
        self.pedidos_asignados.get(pedido_ix).camion_ix = None
        self.carga_total -= self.pedidos_asignados.get(pedido_ix).carga
        self.cantidad_pedidos -= 1
        self.pedidos_asignados.pop(pedido_ix)
    
    def get_carga_total(self):
        return self.carga_total
    
    def get_costo(self):
         
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
        if self.carga_total != 0:
            return self.get_costo()/self.carga_total
        else:
            return None
    
    def count_pedidos(self):
        return self.cantidad_pedidos
    
    def get_ix_pedidos(self):
        return list(self.pedidos_asignados.keys())
    
    def get_pedidos(self):
        return list(self.pedidos_asignados.values())
    
    def get_pedido(self, ix):
        return self.pedidos_asignados.get(ix)
    
    def reset_pedidos(self):
        self.pedidos_asignados.clear()
        self.carga_total = 0
        self.cantidad_pedidos = 0
        
        
        
        
        
class Pedido(object):
    
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
        return self.ix
    
    def get_carga(self):
        return self.carga
    
    def distancia(self, other):
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**(1/2)
        return round(dist, 1)
    
    
    
class Ruteo(object):
    
    def __init__(self, camiones_dict, pedidos_dict, random_state):
        self.camiones = camiones_dict
        self.pedidos = pedidos_dict
        self.random_state = random_state
        
    def get_ix_camiones(self):
        return list(self.camiones.keys())
    
    def get_ix_pedidos(self):
        return list(self.pedidos.keys())
    
    def get_camiones(self):
        return list(self.camiones.values())
    
    def get_pedidos(self):
        return list(self.pedidos.values())
    
    def get_camion(self, ix):
        return self.camiones.get(ix)
    
    def get_pedido(self, ix):
        return self.pedidos.get(ix)
    
        
    def get_solucion_inicial(self, mode):
        
        random.seed(self.random_state)
        #np.random.seed(self.random_state)
        
        if mode == "1":
            for camion in self.get_camiones():
                for pedido in self.get_pedidos():
                    camion.add_pedido_checked(pedido)
                    
        elif mode == "2":     
            # CREO UNA LISTA DE IX DE PEDIDOS MEZCLADA AL AZAR 
            # PARA CADA PEDIDO INTENTO METERLO EN CADA CAMION AL AZAR (CAMIONES MEZCLADOS)
            ix_pedidos = random.sample(self.get_ix_pedidos(), len(self.get_ix_pedidos()))
            
            for ix_pedido in ix_pedidos:
                ix_camiones = random.sample(self.get_ix_camiones(), len(self.get_ix_camiones()))
                for ix_camion in ix_camiones:
                    self.get_camion(ix_camion).add_pedido_checked(pedido)
            
        else:
            for camion in self.get_camiones():
                for pedido in self.get_pedidos():
                    camion.add_pedido_checked(pedido)
                    
                    
    def generar_vecino(self, random_state):
        
        # Genera una lista de repeticiones (deep copies) de la solucion inicial.
        # Usa una estrategia para modificar cada una de las copias para tener soluciones vecinas factibles.
        
        #np.random.seed(random_state)
        random.seed(random_state)
        
        camion_index = random.randint(0, len(self.camiones)-1)
        pedido_index = random.randint(0, len(self.pedidos)-1)
        
        pass
        
    
    # PARA CAMBIAR TODA ESTA PARTE
    # GENERAR UN DATAFRAME CON TODOS LOS DATOS.
    def set_results(self):
        self.set_carga_total()
        self.set_costo_camiones()
        self.set_costo_oportunidad()
        self.set_costo_total()
        self.set_costo_total_tn()
        self.set_ahorro()
        
    def get_results(self):
        self.set_results()
        print("--Resultados--")
        print(f"Carga Total {self.carga_total} tn")
        print(f"Costo Camiones {self.costo_camiones} $")
        print(f"Costo Oportunidad {self.costo_oport} $")
        print(f"Costo Total {self.costo_total} $")
        print(f"Costo Total por tn {self.costo_total_tn} $")
        print(f"Ahorro {self.ahorro*100}%")
    
    def set_carga_total(self):
        self.carga_total = sum([camion.get_carga_total() for camion in self.camiones.values()])
        
    def set_costo_camiones(self):
        self.costo_camiones = sum([camion.get_costo() for camion in self.camiones.values()])
        
    def set_costo_oportunidad(self):
        carga_no_asignada = sum([pedido.get_carga() for pedido in self.pedidos.values() if not pedido.asignado])
        self.costo_oport = carga_no_asignada*3000
        
    def set_costo_total(self):
        self.costo_total = self.costo_camiones + self.costo_oport
    
    def set_costo_total_tn(self):
        self.costo_total_tn = round(self.costo_total/self.carga_total, 2)
        
    def set_ahorro(self):
        self.ahorro = round((self.costo_total_tn - 1200)/1200, 4)
        
        
def generar_vecinos(sol_inicial, n, random_state):
    # Genera una lista de repeticiones (deep copies) de la solucion inicial.
    # Usa una estrategia para modificar cada una de las copias para tener soluciones vecinas factibles.
    random.seed(random_state)
    #np.random.seed(random_state)
    vecinos = []
    
    for i in range(n):
        vecino = copy.deepcopy(sol_inicial)
        
        camion_index = random.randint(0, len(vecino.camiones)-1)
        pedido_index = random.randint(0, len(vecino.pedidos)-1)