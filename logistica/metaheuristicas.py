import time
import copy
import math
import random
from tqdm import tqdm

def sa(ruteo_inicial, t_inicial, t_final, k, iters, prob=1):
    """
    Esta función permite llevar a cabo la metaheurística de recocido simulado, definiendo número de iteraciones
    en cada temperatura y factor k de reducción de temperatura.

    Args:
        ruteo_inicial (Ruteo): Instancia de Ruteo con una solución incial generada.
        t_inicial (int): Temperatura inicial del proceso.
        t_final (int): Temperatura final del proceso.
        k (int): Factor de reducción de temperatura (en unidades de temperatura).
        iters (int): Número de iteraciones para una temperatura.
        prob (int, optional): Argumento opcional en la generación de vecinos. Defaults to 1.

    Returns:
        tuple: Devuelve dos objetos:
               - La instancia de Ruteo con la mejor solución encontrada.
               - Un diccionario que contiene la sucesión de soluciones evaluadas y la sucesión de mejores soluciones. Además guarda el tiempo de ejecución.
    """
    start = time.time()
    
    best_solution = copy.deepcopy(ruteo_inicial)
    actual_solution = copy.deepcopy(ruteo_inicial)
    
    solution_history = {}
    solution_history["history_actual"] = []
    solution_history["history_best"] = [best_solution.costo_total_tn]
    
    temps = sorted([t for t in range(t_final, t_inicial+k, k)], reverse=True)
    #print(temps)
    
    for t in tqdm(temps):     
        for i in range(iters):
            new_solution = copy.deepcopy(actual_solution)
            new_solution.get_vecino(prob=prob)
            new_solution._set_results()
            
            if new_solution.costo_total_tn > actual_solution.costo_total_tn:
                delta = actual_solution.costo_total_tn - new_solution.costo_total_tn 
                #print(delta)
                #print(math.exp(delta/t))
                if math.exp(delta/t) > random.uniform(0,1):
                    actual_solution = copy.deepcopy(new_solution)
                    solution_history["history_actual"].append(actual_solution.costo_total_tn)
                
            else:
                actual_solution = copy.deepcopy(new_solution)
                solution_history["history_actual"].append(actual_solution.costo_total_tn)
                
            if actual_solution.costo_total_tn < best_solution.costo_total_tn:
                best_solution = copy.deepcopy(actual_solution)
                solution_history["history_best"].append(best_solution.costo_total_tn)
            
    
    end = time.time()
    solution_history["time"] = end-start
    
    return (best_solution, solution_history)