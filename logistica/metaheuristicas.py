import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
from tqdm import tqdm
import time
import copy
import math
import random




def sa(ruteo_inicial, t_inicial, t_final, k, iters, temp_mode="linear", prob=1, random_state=None):
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
    if random_state is not None:
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
    solution_history["iters"] = len(solution_history["actual_sol"])
    
    return (best_solution, solution_history)


def linear_temps(t_inicial, t_final, k):
    temps = list(-np.sort(-np.linspace(t_final, t_inicial+t_final, k)))
    return temps

def non_linear_temps(t_inicial, k):
    temps = [t_inicial * (1-(1/(1+np.exp(-i)))) for i in np.linspace(-6.5, 7, k)]
    return temps


def get_history_df(history):
    df_history = pd.DataFrame({"temp":history["temp"],
                           "actual_sol":history["actual_sol"],
                           "new_sol":history["new_sol"]})

    df_history = (df_history
                .assign(best_sol = lambda df_: df_.actual_sol.cummin(),
                        delta = lambda df_: df_.actual_sol - df_.new_sol,
                        p = lambda df_: np.exp(df_.delta/df_.temp))
                .assign(p = lambda df_: np.round(np.where(df_.p > 1, 1, df_.p) ,2)))

    return df_history


def make_history_plots(history):
    
    if isinstance(history, dict):
        df_history = get_history_df(history)
    else:
        df_history = history
    
    fig1 = px.line(df_history,
                   x=df_history.index,
                   y=["new_sol", "actual_sol"],
                   color_discrete_map={"new_sol":"#4e68c7", "actual_sol":"#db8344"})

    fig2 = px.line(df_history,
                   x=df_history.index,
                   y=["delta", "p"],
                   color_discrete_map={"delta":"#4e68c7", "p":"#d43a22"})

    fig3 = px.line(df_history,
                   x=df_history.index,
                   y=["temp"],
                   color_discrete_map={"temp":"#4e68c7"})

    fig4 = px.line(df_history,
                   x=df_history.index,
                   y=["best_sol"],
                   color_discrete_map={"best_sol":"#22a7d4"})
    
    fig = make_subplots(rows=2, cols=2,
                        column_widths=[0.5, 0.5],
                        row_heights=[0.5, 0.5],
                        subplot_titles=['Actual y Nueva Solución', 
                                        'Temperatura', 
                                        'Delta y Probabilidad de Cambio', 
                                        'Mejor Solución'],
                        shared_xaxes=True)

    traces = []
    for i, figure in enumerate([fig1, fig2, fig3, fig4]):
        traces.append([])
        for trace in range(len(figure["data"])):
            traces[i].append(figure["data"][trace])

    ubicacion = {0:[1,1], 1:[2,1], 2:[1,2], 3:[2,2]}

    for i in range(4):
        for trace in traces[i]:
            fig.append_trace(trace, row=ubicacion[i][0], col=ubicacion[i][1])

    fig.update_layout(template="plotly_white",
                      height=800,
                      width=1600,
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.08,
                                  xanchor="center",
                                  x=0.5),
                      hovermode="x unified")

    fig.show()





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