import typing
import unittest

from tegelaar import Tegelaar



class TestTegelaar(unittest.TestCase):

    def test_rotate_tile(self):
        height = 30
        width = 20
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        self.assertEqual(tg.rotate_tile((30,10)), (10,30))
        self.assertEqual(tg.rotate_tile((50,50)), (50,50))

    def test_get_price(self):
        height = 30
        width = 20
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        for t in tiles:
            rt = tg.rotate_tile(t)

            self.assertEqual(tg.get_price(t), t[0]*t[1])
            self.assertEqual(tg.get_price(rt), t[0]*t[1])

    def test_tile_is_possible(self):
        height = 30
        width = 20
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10)]
        prices = {x:x[0]*x[1] for x in tiles}

        budget = float(100)
        tg = Tegelaar(width, height, tiles, prices, budget)

        p1, tile1, p2, tile2 = (0,0), (10,10), (0,5), (5,5)
        tg.prices[(10,10)] = 0
        self.assertFalse(tg.tile_is_possible(tile=(10,10), cost_tile=0, total_cost=20, rem_surface=10)) # no space for tile - no need to invest current solution
        prices[(10,10)] = 1000
        self.assertFalse(tg.tile_is_possible(tile=(10,10), cost_tile=1000, total_cost=20, rem_surface=10)) # not  enough budget

        prices[(10,10)] = 10
        self.assertTrue(tg.tile_is_possible(tile=(10,10), cost_tile=10, total_cost=20, rem_surface=150)) # enough space for tile - no need to invest current solution
        self.assertTrue(tg.tile_is_possible(tile=(10,10), cost_tile=10, total_cost=20, rem_surface=110)) # enough budget

    def test_tiles_overlap(self):
        height = 30
        width = 20
        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10), (10,20):(10,20)}
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10),(10,20),(10,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        self.assertTrue(tg.has_overlap(position=(0,30), tile=(20,10), solution=current_solution))

        p1, tile1, p2, tile2 = (0,0), (10,10), (0,5), (5,5)
        self.assertTrue(tg.tiles_overlap(p1, tile1, p2, tile2))
        p1, tile1, p2, tile2 = (0,0), (10,10), (10,10), (5,5)
        self.assertFalse(tg.tiles_overlap(p1, tile1, p2, tile2))


    def test_has_overlap(self):
        height = 40
        width = 20
        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10), (10,20):(10,20)}
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10),(10,20),(10,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        self.assertTrue(tg.has_overlap(position=(0,30), tile=(20,10), solution=current_solution))
        self.assertFalse(tg.has_overlap(position=(0,30), tile=(10,10), solution=current_solution))


    def test_has_overlap_own_case(self):
        height = 40
        width = 20
        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10), (10,20):(10,20)}
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10),(10,20),(10,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        self.assertTrue(tg.has_overlap(position=(5,10), tile=(10,10), solution=current_solution))


    def test_can_place_tile(self):
        height = 40
        width = 20
        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10)}
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10),(10,20),(10,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)

        self.assertFalse(tg.can_place_tile(0, 20, (21,10), current_solution)) # out of

        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10), (10,20):(10,20)}
        self.assertFalse(tg.can_place_tile(0, 20, (20,10), current_solution)) # overlap

        # no overlap, can place
        self.assertTrue(tg.can_place_tile(0,20,(10,10), current_solution))

    def test_add_tile_to_solution(self):
        height = 40
        width = 20
        current_solution = {(0,0): (10, 20), (10,0): (10, 10), (10,10):(10,10), (10,20):(10,20)}
        tiles = [(30,10), (50,50), (60,60), (10,10), (10,10), (10,10),(10,20),(10,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        new_moves_answer = tg.add_tile_to_solution(0,20,(10,10), set([(0,20)]), partial_solution=current_solution)
        new_moves = [(10, 20), (0, 30)]
        # Check if all new moves returned by the function is correct
        for m in new_moves_answer:
            self.assertTrue(m in new_moves)

        real_solution = {(0, 0): (10, 20), (10, 0): (10, 10), (10, 10): (10, 10), (10, 20): (10, 20), (0, 20): (10, 10)}
        # check if the partial solution dictionary was updated correctly
        for k,v in real_solution.items():
            self.assertTrue(k in current_solution)
            self.assertTrue(current_solution[k] == v)



    def test_backtracking_easy_square(self):
        # 3 tiles of 20x20 by 3 tiles of 20x20
        height = 60
        width = 60
        tiles = [(20,20) for _ in range(8)] + [(30,10)] + [(20,20)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, total_cost = tg.start_search()
        solution = {(0, 0): (20, 20), (0, 20): (20, 20), (0, 40): (20, 20), (20, 20): (20, 20), (20, 0): (20, 20), (40, 20): (20, 20), (40, 0): (20, 20), (40, 40): (20, 20), (20, 40): (20, 20)}
        solution_cost = 3600
        self.assertEqual(tiling_pattern, solution)
        self.assertEqual(total_cost, solution_cost)

    def test_backtracking_no_solution(self):
        height = 60
        width = 60
        tiles = [(20,20) for _ in range(2)]
        prices = {x:x[0]*x[1] for x in tiles}
        budget = float("inf")
        tg = Tegelaar(width, height, tiles, prices, budget)
        tiling_pattern, cost = tg.start_search()
        self.assertIsNone(tiling_pattern)






    