import unittest
from SearchAlgorithm import *
from utils import *
import os


def create_path_with_cost_g(list_nodes, cost_g):
    path = Path(list_nodes)
    path.g = cost_g
    return path

def print_paths(new_paths, list_of_path_removed):
    print('\nNew expanded paths:')
    print_list_of_path_with_cost(new_paths)
    print('List of paths:')
    print_list_of_path_with_cost(list_of_path_removed)


class TestCases(unittest.TestCase):
    ROOT_FOLDER = '../CityInformation/Lyon_smallCity/'

    def setUp(self):
        map_ = read_station_information(os.path.join(self.ROOT_FOLDER, 'Stations.txt'))
        connections = read_cost_table(os.path.join(self.ROOT_FOLDER, 'Time.txt'))
        map_.add_connection(connections)

        info_velocity_clean = read_information(os.path.join(self.ROOT_FOLDER, 'InfoVelocity.txt'))
        map_.add_velocity(info_velocity_clean)

        self.map = map_

    def test_Expand(self):
        expanded_paths = expand(Path(7), self.map)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11]), Path([13, 12, 13])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 8]),
                                          Path([14, 13, 8, 12, 11]),
                                          Path([14, 13, 8, 12, 13])])

    def test_RemoveCycles(self):
        expanded_paths = expand(Path(7), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([7, 6]), Path([7, 8])])

        expanded_paths = expand(Path([13, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([13, 12, 8]), Path([13, 12, 11])])

        expanded_paths = expand(Path([14, 13, 8, 12]), self.map)
        expanded_paths = remove_cycles(expanded_paths)
        self.assertEqual(expanded_paths, [Path([14, 13, 8, 12, 11])])

    def test_depth_first_search(self):
        route1 = depth_first_search(2, 7, self.map)
        route2 = depth_first_search(13, 1, self.map)
        route3 = depth_first_search(5, 12, self.map)
        route4 = depth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 8, 7, 6, 5, 2, 1]))
        self.assertEqual(route3, Path([5, 2, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 8, 7, 6, 5, 2, 10]))

    def test_breadth_first_search(self):
        route1 = breadth_first_search(2, 7, self.map)
        route2 = breadth_first_search(13, 1, self.map)
        route3 = breadth_first_search(5, 12, self.map)
        route4 = breadth_first_search(14, 10, self.map)

        self.assertEqual(route1, Path([2, 5, 6, 7]))
        self.assertEqual(route2, Path([13, 12, 11, 10, 2, 1]))
        self.assertEqual(route3, Path([5, 10, 11, 12]))
        self.assertEqual(route4, Path([14, 13, 12, 11, 10]))

    def test_calculate_cost(self):
        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=0)
        self.assertEqual([path.g for path in updated_paths], [1, 1])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=1)
        self.assertEqual([path.g for path in updated_paths], [4.21429, 6.03739])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=2)
        self.assertEqual([path.g for path in updated_paths], [59.000060000000005, 84.52346])

        list_of_path = [Path([7, 6]), Path([7, 8])]
        updated_paths = calculate_cost(list_of_path, self.map, type_preference=3)
        self.assertEqual([path.g for path in updated_paths], [0, 0])

    def test_uniform_cost_search(self):
        route = uniform_cost_search(9, 3, self.map, 0)
        self.assertEqual(route, Path([9, 8, 7, 6, 5, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 1)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 2)
        self.assertEqual(route, Path([9, 8, 12, 11, 10, 2, 3]))

        route = uniform_cost_search(9, 3, self.map, 3)
        self.assertEqual(route, Path([9, 8, 7, 6, 5, 2, 3]))

    def test_calculate_heuristics(self):
        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=0)
        self.assertEqual([path.h for path in updated_paths], [1, 0, 1])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=1)
        self.assertEqual([path.h for path in updated_paths], [1.8544574262244504, 0.0, 0.6273597428219158])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=2)
        self.assertEqual([path.h for path in updated_paths], [83.45058418010026, 0.0, 28.231188426986208])

        expanded_paths = [Path([12, 8, 7]), Path([12, 8, 9]), Path([12, 8, 13])]
        updated_paths = calculate_heuristics(expanded_paths, self.map, destination_id=9, type_preference=3)
        self.assertEqual([path.h for path in updated_paths], [0, 0, 1])

    def test_remove_redundant_path(self):
        # Necessary setup for testing
        path_1 = create_path_with_cost_g([12, 8, 7], 84.52)
        path_2 = create_path_with_cost_g([12, 8, 13, 9], 235.23)
        path_3 = create_path_with_cost_g([12, 8, 15, 11], 350.12)
        # these are the paths you have to check
        list_of_path = [path_1, path_2, path_3]
        # this the expanded path of path_1
        expand_paths = [create_path_with_cost_g([12, 8, 7, 11], 124.52),
                        create_path_with_cost_g([12, 8, 7, 15], 222.52)]
        # Now imagine you have the cost dictionary
        cost_dict = {11: 350.12, 13: 135.87, 7: 169.04692, 9: 235.23, 15: 400}
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        # If you would like to print the paths uncomment the line below
        # print_paths(new_paths, list_of_path_removed)
        self.assertEqual(list_of_path_removed, [path_1, path_2])
        self.assertEqual(new_paths, expand_paths)

        cost_dict = {11: 350.12, 13: 135.87, 7: 84.52, 9: 235.23, 15: 200.10}
        expand_paths = [create_path_with_cost_g([12, 8, 7, 11], 124.52),
                        create_path_with_cost_g([12, 8, 7, 15], 222.52)]
        new_paths, list_of_path_removed, _ = remove_redundant_paths(expand_paths, list_of_path, cost_dict)
        # self.print_paths(new_paths, list_of_path_removed)
        self.assertEqual(list_of_path_removed, [path_1, path_2])
        self.assertEqual(new_paths, expand_paths[0:1])


    def test_coord2station(self):
        station_id = coord2station([105, 205], self.map)
        self.assertEqual(station_id, [8, 12, 13])

        station_id = coord2station([300, 111], self.map)
        self.assertEqual(station_id, [3])

        station_id = coord2station([10, 11], self.map)
        self.assertEqual(station_id, [1])

    def test_Astar(self):
        # If you want to see the optimal_path's route and f-cost,
        # uncomment the print functions below

        optimal_path = Astar(8, 1, self.map, 0)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([8, 7, 6, 5, 2, 1]))
        self.assertEqual(optimal_path.f, 5)

        optimal_path = Astar(2, 6, self.map, 1)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([2, 5, 6]))
        self.assertEqual(optimal_path.f, 27.14286)

        optimal_path = Astar(9, 4, self.map, 2)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([9, 8, 12, 11, 10, 5, 4]))
        self.assertEqual(optimal_path.f, 326.53992)

        optimal_path = Astar(3, 14, self.map, 3)
        # print(optimal_path.route, optimal_path.f)
        self.assertTrue(optimal_path == Path([3, 2, 10, 11, 12, 13, 14]) or
                        optimal_path == Path([3, 2, 5, 6, 7, 8, 13, 14]))
        self.assertEqual(optimal_path.f, 2)

    '''def test_Astar_multiple_origins(self):
        # If you want to see the optimal_path's route and f-cost,
        # uncomment the print functions below

        optimal_path = Astar_multiple_origins([108, 206], 1, self.map, 0)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([12, 11, 10, 2, 1]))
        self.assertEqual(optimal_path.f, 4)

        optimal_path = Astar_multiple_origins([140, 56], 6, self.map, 1)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([5, 6]))
        self.assertEqual(optimal_path.f, 7.14286)

        optimal_path = Astar_multiple_origins([82, 217], 4, self.map, 2)
        # print(optimal_path.route, optimal_path.f)
        self.assertEqual(optimal_path, Path([9, 8, 12, 11, 10, 5, 4]))
        self.assertEqual(optimal_path.f, 326.53992)

        optimal_path = Astar_multiple_origins([167, 64], 14, self.map, 3)
        # print(optimal_path.route, optimal_path.f)
        self.assertTrue(optimal_path == Path([3, 2, 10, 11, 12, 13, 14]) or
                        optimal_path == Path([3, 2, 5, 6, 7, 8, 13, 14]))
        self.assertEqual(optimal_path.f, 2)'''


if __name__ == "__main__":
    unittest.main()
