from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    properes = coord2station([42,3],map)
    print(properes)
    print()
    print()

    camins = remove_cycles([Path([5, 7, 1, 6, 2]), Path([5, 7, 1, 6, 8]), Path([5, 7, 1, 6, 5]), Path([5, 7, 1, 6, 7]), Path([5, 7, 1, 6, 3])])
    print(camins)
    print_list_of_path_with_cost(camins)
    print()
    print()

    amplada = breadth_first_search(21, 16, map)
    print(amplada.route)
    print()
    print()
    cost = calculate_cost([Path([11, 12, 13, 14])], map, 2)
    print_list_of_path_with_cost(cost)
    print()
    print()

    c = calculate_heuristics([Path([17, 16, 15, 14, 13, 12, 11, 18, 19, 20, 21, 22])], map, 22, 1)
    print([path.h for path in c])
    print_list_of_path_with_cost(c)
    AS = Astar(17, 22, map, 1)
    print()
    print()
    AS10 = Astar(2, 13, map, 1)
    print_list_of_path_with_cost([AS10])
    print()
    print()
    expanded = [Path([1, 5, 4]), Path([1, 5, 7]), Path([1, 5, 2]), Path([1, 5, 8, 3])]
    llista = [Path([1, 5, 8, 4]), Path([1, 5, 8, 7]), Path([1, 5, 8, 2]), Path([1, 5, 8, 3])]
    TC = {}
    TC[5] = 2.95
    TC[8] = 45.53
    TC[4] = 37.27
    TC[7] = 38.46
    TC[2] = 9.56
    redundant = remove_redundant_paths(expanded, llista, TC)

    cada = calculate_cost([Path([11, 12, 13, 14])], map, 2)
    print_list_of_path_with_cost(cada)



    ### this code is just for you, you won't have to upload it after the exam ###


    #this is an example of how to call some of the functions that you have programed
    #example_path=uniform_cost_search(9, 3, map, 1)
    #print_list_of_path_with_cost([example_path])

