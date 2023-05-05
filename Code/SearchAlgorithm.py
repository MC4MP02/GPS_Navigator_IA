# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1633330'
__group__ = 'DJ.08'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2022 - 2023
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    ruta_final = [] #Creacio de la llista
    for i in map.connections[path.route[-1]]:
        expanded = copy.deepcopy(path) 
        expanded.route.append(i)
        ruta_final.append(expanded)
    
    return ruta_final

def remove_cycles(path_list):
    llista = copy.deepcopy(path_list) #Creacio de la llista i inicialitzacio amb la copia del path
    for i in path_list:
        for j in i.route[:len(i.route)-1]:
            if j == i.route[-1]:
                llista.remove(i) #Si esta repetit al path (doble for) s'elimina
    return llista

def insert_depth_first_search(expand_paths, list_of_path):
    return expand_paths + list_of_path

def depth_first_search(origin_id, destination_id, map):
    llista = []
    origin_path = Path(origin_id) #Creacio de objecte tipus Path buit
    llista.append(origin_path)
    
    while (llista[0].route[-1] != destination_id) and llista:
        C = llista[0]
        E = expand(C, map) #Expand del cap de la llista
        E = remove_cycles(E) #Remove dels cicles per evitar errors
        llista = insert_depth_first_search(E, llista[1:]) #Insert a la llista de la cua sense cicles
        
    if llista:
        return llista[0]
    else:
        print("NO existeix solucio")

def insert_breadth_first_search(expand_paths, list_of_path):
    return list_of_path + expand_paths

def breadth_first_search(origin_id, destination_id, map):
    llista = []
    origen = Path(origin_id)
    llista.append(origen)
    
    while (llista[0].route[-1] != destination_id) and llista:
        C = llista[0]
        E = expand(C, map) #Expand del cap de la llista
        E = remove_cycles(E) #Remove dels cicles per evitar errors
        llista = insert_breadth_first_search(E, llista[1:]) #Insert a la llista de la cua sense cicles
        
    if llista:
        return llista[0]
    else:
        print("NO existeix solucio")

def coord2station(coord, map):
    stations_dist = []  # Creacio de la llista
    for key, value in map.stations.items():  # for al diccionari de stations
        distance = math.sqrt(
            (coord[0] - value['x']) ** 2 + (coord[1] - value['y']) ** 2)  # Calcul de la funcio euclidean_dist
        stations_dist.append((distance, key))

    stations_dist.sort()  # Ordenacio de la llista per poder operar amb ella
    min_distance = stations_dist[0][1]
    min_distance = [stat[1] for stat in stations_dist if stat[0] == stations_dist[0][0]]

    return min_distance

def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    #Switch case con el type_preference
    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)
    if type_preference == 1:
        for path in expand_paths:
            time = map.connections[path.route[-2]][path.route[-1]] #El tiempo viene dado por la connexion entre dos estaciones en "connections"
            path.update_g(time)
    if type_preference == 2:
        for path in expand_paths:
            v1 = map.stations[path.route[-1]]['velocity'] #Calculamos la velocidad de las dos linias de las estaciones
            v2 = map.stations[path.route[-2]]['velocity']
            if v1 == v2: #Si es igual se actualiza el coste con el tiempo * velocidad
                time = map.connections[path.route[-2]][path.route[-1]]
                path.update_g(time * v1)
    if type_preference == 3:
        for path in expand_paths:
            if map.stations[path.route[-1]]['line'] != map.stations[path.route[-2]]['line']: #Si la linia es diferente se actualiza (hay transbordo)
                path.update_g(1)
    return expand_paths

def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    for path in expand_paths:
        cost = path.g
        i = 0
        while i < len(list_of_path) and cost >= list_of_path[i].g:
            i += 1
        list_of_path.insert(i, path)

    return list_of_path

def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista = []
    origen = Path(origin_id)
    llista.append(origen)
    #Seguir el algoritmo visto en teoria
    while (llista[0].route[-1] != destination_id) and llista:
        C = llista[0]
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        llista = insert_cost(E, llista[1:])

    if llista:
        return llista[0]
    else:
        print("NO existeix solucio")

def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    # Switch case con el type_preference
    if type_preference == 0:
        for path in expand_paths:
            if path.route[-1] == destination_id or path.route[-1] in map.connections[destination_id].keys(): #comprobacion si no estamos en el destino y si la estacion existe
                path.update_h(0)
            else:
                path.update_h(1)
    if type_preference == 1:
        for path in expand_paths:
            #Calculamos la distancia con la funcion euclidiana
            distance = math.sqrt((map.stations[path.route[-1]]['x'] - map.stations[destination_id]['x']) ** 2 + (map.stations[path.route[-1]]['y'] - map.stations[destination_id]['y']) ** 2)
            vmax = 0
            #Calculamos la velocidad maxima de "velocity"
            for i, v in map.velocity.items():
                if v > vmax:
                    vmax = v
            path.update_h(distance/vmax) #cost = distancia / velocidad
    if type_preference == 2:
        for path in expand_paths:
            #Calculo de la distancia con la formula euclidiana
            distance = math.sqrt((map.stations[path.route[-1]]['x'] - map.stations[destination_id]['x']) ** 2 + (map.stations[path.route[-1]]['y'] - map.stations[destination_id]['y']) ** 2)
            path.update_h(distance)
    if type_preference == 3:
        for path in expand_paths:
            if map.stations[path.route[-1]]['line'] != map.stations[destination_id]['line']: #Si la linias son diferentes h = 1
                path.update_h(1)
            else:
                path.update_h(0)

    return expand_paths

def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f() #Se actualiza la f para cada path
    return expand_paths

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    #Seguir el algoritmo visto en teoria
    for path in expand_paths:
        if path.route[-1] in visited_stations_cost:
            CP = visited_stations_cost[path.route[-1]]
            if path.g < CP:
                visited_stations_cost[path.route[-1]] = path.g
                for it in list_of_path:
                    if CP == it.g and it.route[-1] == path.route[-1]:
                        list_of_path.remove(it)
            else:
                expand_paths.remove(path)
    return expand_paths, list_of_path, visited_stations_cost

def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """

    for path in expand_paths:
        cost = path.f
        i = 0
        while i < len(list_of_path) and cost >= list_of_path[i].f:
            i += 1
        list_of_path.insert(i, path)

    return list_of_path
    
def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    llista = []
    origen = Path(origin_id)
    llista.append(origen)
    TCP = {}
    # Seguir el algoritmo visto en teoria
    while (llista[0].route[-1] != destination_id) and llista:
        C = llista[0]
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        E, llista, TCP = remove_redundant_paths(E, llista, TCP)
        E = calculate_heuristics(E, map, destination_id, type_preference)
        E = update_f(E)
        llista = insert_cost_f(E, llista[1:])

    if llista:
        return llista[0]
    else:
        print("NO existeix solucio")

