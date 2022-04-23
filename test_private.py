import time
import typing
import unittest

from tegelaar import Tegelaar


class TestTegelaar(unittest.TestCase):

    def test_backtracking_easy_square_asymetrical_board(self):
        # Test of a asymmetrical board for back-tracking.

        height = 60
        width = 80
        tiles = [(20, 20) for _ in range(11)] + [(30, 10)] + [(20, 20)]
        prices = {x: x[0] * x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        solution = {(0, 0): (20, 20), (0, 20): (20, 20), (0, 40): (20, 20), (20, 20): (20, 20), (20, 0): (20, 20),
                    (40, 20): (20, 20), (40, 0): (20, 20), (40, 40): (20, 20), (20, 40): (20, 20), (60, 0): (20, 20),
                    (60, 20): (20, 20), (60, 40): (20, 20)}
        solution_cost = 4800
        self.assertEqual(tiling_pattern, solution)
        self.assertEqual(total_cost, solution_cost)

    def test_too_expensive_backtracking(self):
        # Test for a too expensive problem within backtracking.

        height = 40
        width = 40
        tiles = [(20, 20), (20, 20), (40, 20)]
        prices = {(20, 20): 400, (40, 20): 800}
        budget = 1200
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        self.assertEqual(tiling_pattern, None)
        self.assertEqual(total_cost, None)

    def test_non_square_solution_backtracking(self):
        # Test for none-square for solution

        height = 60
        width = 60
        tiles = [(60, 20), (60, 20), (60, 20)]
        prices = {x: x[0] * x[1] for x in tiles}
        budget = 100000
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        solution_1 = {(0, 0): (60, 20), (0, 20): (60, 20), (0, 40): (60, 20)}
        solution_2 = {(0, 0): (60, 20), (20, 0): (60, 20), (40, 0): (60, 20)}
        solution_cost = 3600

        tiling_outcome = False

        # Two possible tiling-solutions are possible, therefore this statement.
        if tiling_pattern == solution_1 or tiling_pattern == solution_2:
            tiling_outcome = True

        self.assertTrue(tiling_outcome)
        self.assertEqual(total_cost, solution_cost)


    """
    These two functions below are used for the report to get the execution times of the algorithm. 
    They are commented out because of the long run time of the function. 
    
    Due to 
    
    """



    def function_for_exe_times(self, index):
        height = 2000000
        width = 1000000
        tile_amount = int(4 ** index)
        tile_heigth = 2000000 / (2 ** index)
        tile_width = 1000000 / (2 ** index)

        print(f"Tile amount{tile_amount} -- tile: ({tile_width, tile_heigth}")

        tiles = [(tile_width, tile_heigth) for _ in range(tile_amount)]
        prices = {x: x[0] * x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        print(tiling_pattern)

    def test_get_exe_times(self):

        values = [i/2 for i in range(2,20)]

        for value in values:
            starting_time = time.time()
            self.function_for_exe_times(value)
            print("--- %s seconds ---" % (time.time() - starting_time))

