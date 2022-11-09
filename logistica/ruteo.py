import pandas as pd
import numpy as np
import random
from .componentes import Camion
from .componentes import Pedido

class Ruteo(object):
    """ 
    La clase Ruteo contiene toda la información de camiones disponibles y pedidos requeridos:
        - camiones: Diccionario de camiones disponibles identificados por su ix.
        - pedidos: Diccionario de pedidos disponibles identificados por su ix.
        - costo de oportunidad: Costo de pedidos no asignados en $/tn.
        - presupuesto: Presupuesto previsto en $/tn.
        - random_state: Permite definir la semilla para la generación de valores aleatorios.
    """
    
    def __init__(self, df_camiones, df_pedidos, costo_oportunidad, presupuesto):
        self.camiones = self._load_camiones(df_camiones)
        self.pedidos = self._load_pedidos(df_pedidos)
        self.costo_oportunidad = costo_oportunidad
        self.presupuesto = presupuesto
        
        # Uso el random state para determinar la generación de solución inicial.
        # self.random_state = random_state
        # random.seed(self.random_state)
        
    def _load_camiones(self, df_camiones):
        """
        Este método genera el diccionario de camiones a partir de un DataFrame.

        Args:
            df_camiones (pd.DataFrame): Dataframe que contiene la información de camiones.
                                        El mismo debe contener las siguientes columnas:
                                        - camion: Contiene el identificador ix del camión.
                                        - carga_max: Carga máxima admitida para cada camión.
                                        - pedidos_max: Cantidad de pedidos máximo admitido para cada camión.
                                        - dist_max: Distancia máxima entre pedidos asignados a un camión.

        Returns:
            dict: Diccionario con los camiones del ruteo.
        """
        dict_camiones = {row.camion:Camion(ix=row.camion, carga_max=row.carga_max, pedidos_max=row.pedidos_max, dist_max=row.dist_max) for _, row in df_camiones.iterrows()}
        return dict_camiones

    def _load_pedidos(self, df_pedidos):
        """
        Este método genera el diccionario de pedidos a partir de un DataFrame.

        Args:
            df_pedidos (pd.DataFrame): Dataframe que contiene la información de pedidos.
                                        El mismo debe contener las siguientes columnas:
                                        - cliente: Contiene el identificador ix del pedido.
                                        - pedidos: Carga de cada pedido.
                                        - coord_x: Coordenada x del cliente.
                                        - coord_y: Coordenada y del cliente.

        Returns:
            dict: Diccionario con los pedidos del ruteo.
        """
        dict_pedidos = {row.cliente:Pedido(ix=row.cliente, x=row.coord_x, y=row.coord_y, carga=row.pedidos) for _, row in df_pedidos.iterrows() if row.pedidos != 0}
        return dict_pedidos
    
    def __str__(self):
        self._set_results()
        return f"--Ruteo--\nCarga Total: {self.carga_total}tn\nCosto Camiones: {self.costo_camiones}$\nCosto Oportunidad: {self.costo_no_asignados}$ \nCosto Total: {self.costo_total}$ \nCosto Total por tn: {self.costo_total_tn}$/tn \nAhorro: {self.ahorro}%"

    def __repr__(self):
        self._set_results()
        return f"--Ruteo--\nCarga Total: {self.carga_total}tn\nCosto Camiones: {self.costo_camiones}$\nCosto Oportunidad: {self.costo_no_asignados}$ \nCosto Total: {self.costo_total}$ \nCosto Total por tn: {self.costo_total_tn}$/tn \nAhorro: {self.ahorro}%"
    
    def get_ix_camiones(self):
        """
        Returns:
            list: Lista de ix de camiones.
        """   
        return list(self.camiones.keys())
    
    def get_ix_pedidos(self):
        """
        Returns:
            list: Lista de ix de pedidos.
        """  
        return list(self.pedidos.keys())
    
    def get_camiones(self):
        """
        Returns:
            list: Lista de camiones.
        """  
        return list(self.camiones.values())
    
    def get_pedidos(self):
        """
        Returns:
            list: Lista de pedidos.
        """          
        return list(self.pedidos.values())
    
    def get_camion(self, ix):
        """
        Returns:
            Camion: Camion con identificador ix.
        """  
        return self.camiones.get(ix)
    
    def get_pedido(self, ix):
        """
        Returns:
            Pedido: Pedido con identificador ix.
        """  
        return self.pedidos.get(ix)
    
    def count_camiones(self):
        """
        Returns:
            int: Cantidad de camiones.
        """  
        return len(self.camiones)
    
    def count_pedidos(self):
        """
        Returns:
            int: Cantidad de pedidos.
        """  
        return len(self.pedidos)
    
        
    def get_solucion_inicial(self, mode="simple", random_state=1):
        """
        Permite generar una solución inicial, es decir, realizar una asignación inicial de pedidos en camiones.
        
        Permite usar varios modos diferentes de generación de solución inicial con el argumento de este método.

        Args:
            mode (_type_): _description_
        """
        
        if mode == "simple":
            self._get_solucion_inicial_simple()
                    
        elif mode == "random":
            self._get_solucion_inicial_random(random_state)     
            
        else:
            self._get_solucion_inicial_simple()
            
        # Generamos los resultados de la solución.
        self._set_results()  
    
    # EXPLICAR Y CHEQUEAR BIEN LAS SOLUCIONES INICIALES.              
    
    def _get_solucion_inicial_simple(self):
        """
        Genera una solución inicial deterministica. 
        Para cada camión, toma cada pedido disponible y lo intenta asignar, siendo asignado si pasa los chequeos.
        Queda definido por el orden de carga de camiones y pedidos.
        """
        for camion in self.get_camiones():
            for pedido in self.get_pedidos():
                camion.add_pedido_checked(pedido)
                
                
    def _get_solucion_inicial_random(self, random_state=None):
        """
        Genera una solución con aleatoriedad.
            1. Mezcla los ix de pedidos de manera aleatoria.
            2. Para cada pedido en el orden aleatorio genera una lista de ix de camiones aleatoria
            3. Para cada camión en orden aleatorio se intenta agregar el pedido. En caso de lograrse
               pasa al siguiente pedido en orden aleatorio volviendo a 2.
            
        Prueba introducir todos los pedidos en todos los camiones en orden aleatorio.
        """
        # Definimos la semilla.
        if random_state is not None:
            random.seed(random_state)
        # Identificadores aleatorios de pedidos.
        ix_pedidos_rnd = random.sample(self.get_ix_pedidos(), self.count_pedidos())
        
        for ix_pedido in ix_pedidos_rnd:
            pedido = self.get_pedido(ix_pedido)
            ix_camiones_rnd = random.sample(self.get_ix_camiones(), self.count_camiones())
            
            for ix_camion in ix_camiones_rnd:
                self.get_camion(ix_camion).add_pedido_checked(pedido)
                
                if pedido.asignado:
                    break
    
    
    def get_vecino(self, prob=1):
        """
        Realiza una modificación en la instancia de la solución, creando una nueva solución similar y válida de ruteo.
        
            1. Se selecciona un pedido al azar entre todos los pedidos. Este es el pedido a modificar (pedido_mod).
            2. Chequeamos si el pedido_mod puede ingresar a un camión de manera directa.
            
            3. Si el pedido ya está asignado:
                a. Obtenemos el ix del camión al que estaba asignado (camion al que le iría el nuevo pedido en caso de reemplazo).
                b. Eliminamos el pedido_mod del camión.
                
                4. Si el pedido_mod entra directamente en otro camion y prob es mayor al valor aleatorio uniforme(0,1):
                   Con prob = 1 (default) el 100% de las veces que entre directamente irá a esos camiones.
                    a. Se lo asigna directamente a alguno de los camiones directos al azar.
                       Si entra de manera directa no hace falta chequear que entre. 
                       No hace falta intercambiar por otro pedido porque entra directo.
                      
                4. Si el pedido no entra directamente en otro camion:
                    a. Se genera una lista de ix de pedidos que podrían ser reemplazados en sus camiones por pedido_mod.
                    b. Se genera una lista de ix de pedidos que podrían ser reemplazados y además que pueden entrar en 
                       el camión en el que estaba pedido_mod.
                    
                    5. Si hay al menos 1 pedido reemplazable posible:
                        a. Se toma un pedido al azar de estos pedidos reemplazables posibles.
                        b. Se elimina al pedido_reemplazo de su camion.
                        c. Se asigna el pedido_mod al camión del pedido_reemplazo.
                        d. Se asigna el pedido_reemplazo en el camión de pedido_mod.
                        
                    5. Si no hay al menos 1 pedido reemplazable posible:
                        a. Se devuelve pedido_mod a su camión original.
                        
            3. Si el pedido no está asignado:
            
                4. Si el pedido_mod entra directamente en otro camion:
                    a. Se lo asigna directamente a alguno de los camiones directos al azar.
                       Si entra de manera directa no hace falta chequear que entre.
                       No hace falta intercambiar por otro pedido porque entra directo.
                       
                4. Si el pedido no entra directamente en otro camion:
                    a. Se genera una lista de ix de pedidos que podrían ser reemplazados en sus camiones por pedido_mod.

                    5. Si hay al menos 1 pedido reemplazable:
                        a. Se toma un pedido al azar de estos pedidos reemplazables.
                        b. Se elimina al pedido_reemplazo de su camion.
                        c. Se asigna el pedido_mod al camión del pedido_reemplazo. El pedido_reemplazo queda sin asignar.

        """
        
        ix_pedido_mod = random.choice(self.get_ix_pedidos())
        pedido_mod = self.get_pedido(ix_pedido_mod)
        
        # Índices de los camiones en los que podría entrar directamente.
        ix_camion_directo = [camion.ix for camion in self.get_camiones() if camion.check_nuevo_pedido(pedido_mod)]
        
        # Si el pedido_mod ya está seleccionado:
        if pedido_mod.asignado:
            
            # Obtenemos el ix del camion al que pertenece pedido_mod
            ix_camion_mod = pedido_mod.camion_ix
            # Eliminamos de su camión a pedido_mod.
            self.get_camion(ix_camion_mod).remove_pedido(pedido_mod.ix)
            
            # Si el pedido_mod entra de manera directa en otro camión, es asignado de manera directa a alguno de esos camiones al azar.
            if len(ix_camion_directo) > 0 and prob >= random.uniform(0,1):
                
                # Se elige un camión directo para cambiar 
                ix_camion_new = random.choice(ix_camion_directo)
                # No hace falta chequear de que entre porque fue revisado previamente.
                self.get_camion(ix_camion_new).add_pedido(pedido_mod)
                
            # Si el pedido no entra directamente en un camión debemos reemplazar pedidos.
            else:
                
                ix_pedidos_reemplazables = []
                
                # Obtengo todos los ix de pedidos que podrían ser reemplazados por pedido_mod en sus camiones.
                for camion in self.get_camiones():
                    ix_pedidos_reemplazables += camion.check_intercambio_pedido(pedido_mod)
                               
                ix_pedidos_reemplazables_posibles = []
                
                # Para que sea posible el intercambio tenemos que quedarnos con los ix de pedidos
                # que entrarían en el camión donde estaba pedido_mod.                
                for ix_pedido_reemplazable in ix_pedidos_reemplazables:
                    pedido_reemplazable = self.get_pedido(ix_pedido_reemplazable)
                    if self.get_camion(ix_camion_mod).check_nuevo_pedido(pedido_reemplazable):
                        ix_pedidos_reemplazables_posibles += ix_pedido_reemplazable
                        
                # Si tengo al menos un reemplazo posible.
                if len(ix_pedidos_reemplazables_posibles) > 0:
                    pedido_reemplazo = self.get_pedido(random.choice(ix_pedidos_reemplazables_posibles))
                    ix_camion_new = pedido_reemplazo.camion_ix
                    self.get_camion(ix_camion_new).remove_pedido(pedido_reemplazo.ix)
                    
                    self.get_camion(ix_camion_new).add_pedido(pedido_mod)
                    self.get_camion(ix_camion_mod).add_pedido(pedido_reemplazo)
                    
                # Si no tengo ningún reemplazo posible reasigno pedido_mod a su camión original.
                else:
                    self.get_camion(ix_camion_mod).add_pedido_checked(pedido_mod)

        # Si el pedido no está asignado:
        else:
            
            # Si el pedido_mod entra de manera directa en otro camión, es asignado de manera directa a alguno de esos camiones al azar.
            if len(ix_camion_directo) > 0:
                
                # Se elige un camión directo para cambiar 
                ix_camion_new = random.choice(ix_camion_directo)
                # No hace falta chequear de que entre porque fue revisado previamente.
                self.get_camion(ix_camion_new).add_pedido(pedido_mod)
                
            # Si el pedido no entra directamente en un camión debemos reemplazar pedidos.   
            else:
                
                ix_pedidos_reemplazables = []
                
                # Obtengo todos los ix de pedidos que podrían ser reemplazados por pedido_mod en sus camiones.
                for camion in self.get_camiones():
                    ix_pedidos_reemplazables += camion.check_intercambio_pedido(pedido_mod)

                # QUE PASA SI NO TENGO NINGUNO
                if len(ix_pedidos_reemplazables) > 0:
                    pedido_reemplazo = self.get_pedido(random.choice(ix_pedidos_reemplazables))
                    ix_camion_new = pedido_reemplazo.camion_ix
                    self.get_camion(ix_camion_new).remove_pedido(pedido_reemplazo.ix)
                    
                    self.get_camion(ix_camion_new).add_pedido(pedido_mod)
        
        #print(f"Pedido {ix_pedido_mod} a Camion {ix_camion_new}")
        
        # Generamos los resultados de la solución.
        self._set_results()    
    
    
    def _set_carga_total(self):
        self.carga_total = sum([camion.get_carga_total() for camion in self.camiones.values()])
        
    def _set_costo_camiones(self):
        self.costo_camiones = sum([camion.get_costo() for camion in self.camiones.values()])
        
    def _set_costo_no_asignados(self):
        carga_no_asignada = sum([pedido.get_carga() for pedido in self.pedidos.values() if not pedido.asignado])
        self.costo_no_asignados = carga_no_asignada*self.costo_oportunidad
        
    def _set_costo_total(self):
        self.costo_total = self.costo_camiones + self.costo_no_asignados
    
    def _set_costo_total_tn(self):
        self.costo_total_tn = round(self.costo_total/self.carga_total, 2)
        
    def _set_ahorro(self):
        self.ahorro = round(((self.costo_total_tn - self.presupuesto)/self.presupuesto)*100, 2)

    def _set_results(self):
        self._set_carga_total()
        self._set_costo_camiones()
        self._set_costo_no_asignados()
        self._set_costo_total()
        self._set_costo_total_tn()
        self._set_ahorro()
        
    def summary_camiones(self, ):
        self._set_results()
        
        pedidos = []
        params = []
        max_peds = 0

        for camion in self.get_camiones():
            n_peds = len(camion.get_ix_pedidos())
            pedidos.append(camion.get_ix_pedidos())
            params.append([camion.get_costo(), camion.get_carga_total()])
            
            if n_peds > max_peds:
                max_peds = n_peds
            
        cols = [f"Cliente {i}" for i in range(1, max_peds+1)]
        ids = [f"Camion {ix}" for ix in self.get_ix_camiones()]
            
        df = pd.DataFrame(pedidos, columns=cols, index=ids)
        df[["Costo", "Carga"]] = params
        df["Costo_tn"] = np.round(df.Costo/df.Carga, 2)
        df.loc["Costo Oportunidad"] = ["", "", "", self.costo_no_asignados, sum([pedido.carga for pedido in self.get_pedidos() if not pedido.asignado]), ""]
        df.loc["Total"] = ["", "", "", self.costo_total, self.carga_total, self.costo_total_tn]
        df["Ahorro"] = [round((costo - self.presupuesto)/self.presupuesto*100, 2) if costo != "" else "" for costo in df.Costo_tn]
        
        return df
        
    def summary_pedidos(self):
        self._set_results()
        
        data_pedidos = []
        for pedido in self.get_pedidos():
            data_pedidos.append([pedido.carga, pedido.asignado, pedido.camion_ix])

        cols = ["Carga", "Asignado", "Camion"]
        ids = [f"Pedido {ix}" for ix in self.get_ix_pedidos()]

        df = pd.DataFrame(data_pedidos, columns=cols, index=ids)
        
        return df
    
    def summary_ruteo(self):
        self._set_results()
        
        metrics = [self.carga_total, self.costo_camiones, self.costo_no_asignados, self.costo_total, self.costo_total_tn, self.ahorro]
        ids = ["Carga Total", "Costo Camiones", "Costo Oportunidad", "Costo Total", "Costo Total por tn", "Ahorro"]
        
        df = pd.DataFrame(metrics, index=ids, columns=[""])
        
        return df
                
        
# def get_results(self):
#     self._set_results()
#     print("--Resultados--")
#     print(f"Carga Total {self.carga_total} tn")
#     print(f"Costo Camiones {self.costo_camiones} $")
#     print(f"Costo Oportunidad {self.costo_no_asignados} $")
#     print(f"Costo Total {self.costo_total} $")
#     print(f"Costo Total por tn {self.costo_total_tn} $")
#     print(f"Ahorro {self.ahorro*100}%")