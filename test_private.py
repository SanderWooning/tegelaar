import typing
import unittest

from tegelaar import Tegelaar
from tegelaar import visualize_solution

tegels = [(20,20), (20,20), (20,20), (30,10)]

empty_array = []
for teg in tegels:
    empty_array.append(teg)

print(empty_array)



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


    def test_bigger_tiling_solution_board(self):
        height = 1000
        width = 1000
        tiles = [(100, 100) for _ in range(50000)]
        prices = {x: x[0] * x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        #visualize_solution(height=height, width=width, solution=tiling_pattern)
