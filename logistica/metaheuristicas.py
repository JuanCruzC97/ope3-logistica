import time
import copy
import math
import random
import numpy as np
from tqdm import tqdm

def sa_old(ruteo_inicial, t_inicial, t_final, k, iters, prob=1, random_state=1):
    """
    Esta función permite llevar a cabo la metaheurística de recocido simulado, definiendo número de iteraciones
    en cada temperatura y factor k de reducción de temperatura.

    Args:
        ruteo_inicial (Ruteo): Instancia de Ruteo con una solución incial generada.
        t_inicial (int or float): Temperatura inicial del proceso.
        t_final (int or float): Temperatura final del proceso.
        k (int or float): Factor de reducción de temperatura (en unidades de temperatura).
        iters (int): Número de iteraciones para una temperatura.
        prob (int, optional): Argumento opcional en la generación de vecinos. Defaults to 1.
        random_state (int, optional): Argumento opcional que permite elegir la semilla de generación de valores pseudoaleatorios. Defaults to 1.

    Returns:
        tuple: Devuelve dos objetos:
               - La instancia de Ruteo con la mejor solución encontrada.
               - Un diccionario que contiene la sucesión de soluciones evaluadas y la sucesión de mejores soluciones. Además guarda el tiempo de ejecución.
    """
    # Definimos la semilla de números aleatorios.
    random.seed(random_state)
    # Medidos el tiempo de comienzo.
    start = time.time()
    
    # Copiamos la solución actual y mejor en nuevos objetos.
    best_solution = copy.deepcopy(ruteo_inicial)
    actual_solution = copy.deepcopy(ruteo_inicial)
    
    # Generamos el diccionario que contiene toda la información del proceso.
    solution_history = {}
    solution_history["history_actual"] = []
    solution_history["history_best"] = [best_solution.costo_total_tn]
    
    # Generamos una lista decreciente de temperaturas según los parámetros de la función.
    temps = list(-np.sort(-np.arange(t_final, t_inicial+k, k)))
    
    # Para cada temperatura:
    for t in tqdm(temps):           
        # Para el número de iteraciones por temperatura elegidas.
        for i in range(iters):
            # Copiamos la solución actual y generamos un vecino.
            new_solution = copy.deepcopy(actual_solution)
            new_solution.get_vecino(prob=prob)
            
            # Si el costo total por tn de la nueva solución es mayor al actual.
            if new_solution.costo_total_tn > actual_solution.costo_total_tn:
                # Calculamos la diferencia de costos.
                delta = actual_solution.costo_total_tn - new_solution.costo_total_tn 
                
                # Si la probabilidad es mayor a una uniforme 0-1
                if math.exp(delta/t) > random.uniform(0,1):
                    # La solución actual pasa a ser la nueva solución con mayor costo.
                    actual_solution = copy.deepcopy(new_solution)
                    solution_history["history_actual"].append(actual_solution.costo_total_tn)
            
            # Si el costo total por tn de la nueva solución es menor al actual.  
            else:
                # La solución actual pasa a ser la nueva solución con menor costo.
                actual_solution = copy.deepcopy(new_solution)
                solution_history["history_actual"].append(actual_solution.costo_total_tn)
            
            # Si la solución actual guardada tiene un menor costo que la mejor solución encontrada.
            if actual_solution.costo_total_tn < best_solution.costo_total_tn:
                # Actualizamos la mejor solución encontrada.
                best_solution = copy.deepcopy(actual_solution)
                solution_history["history_best"].append(best_solution.costo_total_tn)
            
    # Terminamos de medir el tiempo de ejecución y guardamos los resultados.
    end = time.time()
    solution_history["time"] = end-start
    
    return (best_solution, solution_history)


def sa(ruteo_inicial, t_inicial, t_final, k, iters, temp_mode="linear", prob=1, random_state=1):
    """
    Esta función permite llevar a cabo la metaheurística de recocido simulado, definiendo número de iteraciones
    en cada temperatura y factor k de reducción de temperatura.

    Args:
        ruteo_inicial (Ruteo): Instancia de Ruteo con una solución incial generada.
        t_inicial (int or float): Temperatura inicial del proceso.
        t_final (int or float): Temperatura final del proceso.
        k (int or float): Factor de reducción de temperatura (en unidades de temperatura).
        iters (int): Número de iteraciones para una temperatura.
        prob (int, optional): Argumento opcional en la generación de vecinos. Defaults to 1.
        random_state (int, optional): Argumento opcional que permite elegir la semilla de generación de valores pseudoaleatorios. Defaults to 1.

    Returns:
        tuple: Devuelve dos objetos:
               - La instancia de Ruteo con la mejor solución encontrada.
               - Un diccionario que contiene la sucesión de soluciones evaluadas y la sucesión de mejores soluciones. Además guarda el tiempo de ejecución.
    """
    # Definimos la semilla de números aleatorios.
    random.seed(random_state)
    # Medidos el tiempo de comienzo.
    start = time.time()
    
    # Copiamos la solución actual y mejor en nuevos objetos.
    best_solution = copy.deepcopy(ruteo_inicial)
    actual_solution = copy.deepcopy(ruteo_inicial)
    
    # Generamos el diccionario que contiene toda la información del proceso.
    solution_history = {}
    solution_history["actual_sol"] = []
    solution_history["new_sol"] = []
    solution_history["best_sol"] = [best_solution.costo_total_tn]
    solution_history["temp"] = []
    
    # Generamos una lista decreciente de temperaturas según los parámetros de la función.
    #temps = list(-np.sort(-np.arange(t_final, t_inicial+k, k)))
    if temp_mode == "linear":
        temps = linear_temps(t_inicial, t_final, k)
        
    elif temp_mode == "non_linear":
        temps = non_linear_temps(t_inicial, k)
        
    else:
        temps = linear_temps(t_inicial, t_final, k)
    
    # Para cada temperatura:
    for t in tqdm(temps):           
        # Para el número de iteraciones por temperatura elegidas.
        for i in range(iters):
            # Copiamos la solución actual y generamos un vecino.
            new_solution = copy.deepcopy(actual_solution)
            new_solution.get_vecino(prob=prob)
            
            solution_history["actual_sol"].append(actual_solution.costo_total_tn)
            solution_history["new_sol"].append(new_solution.costo_total_tn)
            solution_history["temp"].append(t)
            
            # Calculamos la diferencia de costos.
            delta =  actual_solution.costo_total_tn - new_solution.costo_total_tn
            #print(f"Temp={t}, New_Sol={new_solution.costo_total_tn}, Actual_Sol={actual_solution.costo_total_tn}, Delta={delta}, Prob={math.exp(delta/t)}")
            
            # Si la probabilidad es mayor a una uniforme 0-1
            if math.exp(delta/t) > random.uniform(0,1):
                # La solución actual pasa a ser la nueva solución con mayor costo.
                actual_solution = copy.deepcopy(new_solution)
            
            # Si la solución actual guardada tiene un menor costo que la mejor solución encontrada.
            if actual_solution.costo_total_tn < best_solution.costo_total_tn:
                # Actualizamos la mejor solución encontrada.
                best_solution = copy.deepcopy(actual_solution)
                solution_history["best_sol"].append(best_solution.costo_total_tn)
            
    # Terminamos de medir el tiempo de ejecución y guardamos los resultados.
    end = time.time()
    solution_history["time"] = end-start
    solution_history["random_state"] = random_state
    
    return (best_solution, solution_history)


def linear_temps(t_inicial, t_final, k):
    temps = list(-np.sort(-np.linspace(t_final, t_inicial+t_final, k)))
    return temps

def non_linear_temps(t_inicial, k):
    temps = [t_inicial * (1-(1/(1+np.exp(-i)))) for i in np.linspace(-6.5, 7, k)]
    return temps