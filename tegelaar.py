import typing
from copy import deepcopy


class Tegelaar:
    def __init__(self, width: float, height: float, tiles: typing.List[typing.Tuple[float, float]],
                 prices: typing.Dict[typing.Tuple[float, float], float], budget: float):
        """
        The Tegalaar object, containing all information and functions required for the assignment

        :param width: The width of the rectangular area that has to be tiled
        :param height: The height of the rectangular area that has to be tiled
        :param tiles: A list of tiles (width_tile, height_tile)
        :param prices: A dictionary mapping a tile (width_tile, height_tile) to its price (a float)
        :param budget: The budget of the customer for the tiling
        """
        self.width = width
        self.height = height
        self.budget = budget
        self.tiles = tiles
        self.area = self.width * self.height
        self.prices = prices

    @staticmethod
    def rotate_tile(tile: typing.Tuple[float, float]):
        """
        Rotates a tile 

        :param tile: a tile (width_tile, height_tile)
        """
        return tuple([tile[1], tile[0]])

    def get_price(self, tile: typing.Tuple[float, float]):
        """
        Looks up and returns the price of the given tile.

        :param tile: a tile (width_tile, height_tile)
        """

        if tile in self.prices:
            return self.prices[tile]

        if self.rotate_tile(tile) in self.prices:
            tile = self.rotate_tile(tile)
            return self.prices[tile]

    def tile_is_possible(self, tile: typing.Tuple[float, float], cost_tile: float,
                         total_cost: float, rem_surface: float):

        """
        Function that checks whether the tile can be used based on
           - whether there is enough budget left
           - whether there is enough remaining surface to potentially hold a place for the tile

        :param tile: The tile (tile_width, tile_height)
        :param cost_tile: The cost of the tile
        :param total_cost: The total cost of the current partial solution
        :param rem_surface: The surface that we yet have to fill

        Returns True if the tile can be potentially placed (enough budget and remaining surface)
        and False otherwise
        """

        if tile[0] * tile[1] > rem_surface:
            return False

        if cost_tile + total_cost > self.budget:
            return False

        else:
            return True

    @staticmethod
    def tiles_overlap(pos1: typing.Tuple[float, float], tile1: typing.Tuple[float, float],
                      pos2: typing.Tuple[float, float], tile2: typing.Tuple[float, float]):

        """
        Function that checks whether two tiles are overlapping

        :param pos1: the bottom-left corner (x1, y1) where tile1 starts
        :param tile1: (width_tile1, height_tile1)
        :param pos2: the bottom-left corner (x2, y2) where tile2 starts
        :param tile2: (width_tile2, height_tile2)
        """

        if (pos1[0] >= (pos2[0] + tile2[0])) or \
                ((pos1[0] + tile1[0]) <= pos2[0]) or \
                ((pos1[1] + tile1[1]) <= pos2[1]) or \
                (pos1[1] >= (pos2[1] + tile2[1])):
            return False
        else:
            return True

        # # Step 1. Check if starting position is in other square.
        # if pos1[0] < pos2[0] < (pos1[0] + tile1[0]) and pos1[1] < pos2[1] < (pos1[1] + tile1[1]):
        #     print("Starting position is inside square, will result in a overlap always")
        #     return True
        #
        # # Step 2. Check if the box crosses another tile on the right.
        # if  pos1[1] < pos2[1] < (pos1[1] + tile1[1]) or \
        #     pos1[1] < pos2[1] + tile2[1] < (pos1[1] + tile1[1]):
        #     if pos2[0] + tile2[0] > pos1[0]:
        #         return True
        #
        # # Step 3. Check if
        # if  pos1[0] < pos2[0] < (pos1[0] + tile1[0]) or \
        #     pos1[0] < pos2[0] + tile2[0] < (pos1[0] + tile1[0]):
        #     if pos2[1] + tile2[1] > pos1[0]:
        #         return True
        #
        # else:
        #     return False

    def has_overlap(self, position: typing.Tuple[float, float], tile: typing.Tuple[float, float],
                    solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]]):

        """
        Function that checks whether the tile overlaps with other tiles in the solution
        if it would be placed on the given position

        :param position: the (x,y) coordinate pair where the tile is to be placed
        :param tile: the tile (width_tile1, height_tile1)
        :param solution: the current solution (dictionary mapping positions (x,y)->(tile_width, tile_height))

        Returns True if there is overlap between the tile on position and the other tiles in the solution
        False otherwise
        """

        for key, value in solution.items():
            if self.tiles_overlap(pos1=key, tile1=value, pos2=position, tile2=tile):
                return True

        return False

    def can_place_tile(self, x: float, y: float, tile: typing.Tuple[float, float],
                       partial_solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]]):
        """
        Function that checks whether the tile can be placed in its current orientation
        on location (x,y) based on:
           - whether it exceeds the boundaries of the rectangular surface (self.width, self.height)
           - whether there is overlap with other tiles in the partial solution

        :param x: The x coordinate where the tile will be placed
        :param y: The y coordinate where the tile will be placed
        :param tile: The tile that is being placed on location (x,y)
        :param partial_solution: the partial solution (dictionary mapping positions (x_co,y_co) -> tile)

        Returns True if the tile can be placed (does not violate mentioned constraints)
        and False otherwise
        """

        if x + tile[0] > self.width or y + tile[1] > self.height:
            return False

        if self.has_overlap(solution=partial_solution, position=(x, y), tile=tile):
            return False

        else:
            return True

    def add_tile_to_solution(self, x: float, y: float, tile: typing.Tuple[float, float],
                             pos: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]],
                             partial_solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]]):
        """
        Function that adds a tile in the current orientation to the partial solution
        and adds new positions to the set of positions where new tiles can be placed
        (because 2 new tiles can be placed - on top of the tile on (x,y) and to the right
        of that tile)

        :param x: The x coordinate where the tile will be placed
        :param y: The y coordinate where the tile will be placed
        :param tile: The tile that is being placed on location (x,y)
        :param pos: The set of bottom left corners on which we can potentially put tiles 
                    (initially only (0,0) ~ start filling the area from the bottom left)
        :param partial_solution: the partial solution following the same format as pos
                                 with tiles that have already been placed

        Returns a list of new positions (x', y') that were added to pos. Importantly, new means that
        they were not present before in pos.
        """
        new_positions = []

        partial_solution[(x, y)] = tile

        right_corner = (x + tile[0], y)
        if right_corner not in pos and right_corner[0] < self.width and right_corner[1] < self.height:
            new_positions.append(right_corner)

        top_corner = (x, y + tile[1])
        if top_corner not in partial_solution and top_corner[0] < self.width and top_corner[1] < self.height:
            new_positions.append(top_corner)

        return new_positions

    def recursive_search(self, pos: typing.Set[typing.Tuple[float, float]], rem_surface: float,
                         rem_tiles: typing.List[typing.Tuple[float, float]],
                         solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]],
                         total_cost: float):

        """
        Private function. Feel free to determine your own set of arguments.
        Will not be called from unit tests, but only by this function (recursively) and
        start_search

        TODO: don't forget to update the documentation after you implemented this function

        :param pos: The set of bottom left corners on which we can potentially put tiles 
                    (initially only (0,0) ~ start filling the area from the bottom left)
        :param rem_surface: the remaining surface to be filled
        :param rem_tiles: the remaining tiles that are in the inventory
        :param solution: the partial solution (same structure as pos)
        :param total_cost: the total cost of the partial solution
        """

        for position in pos:
            for tile in rem_tiles:

                config = [tile, self.rotate_tile(tile)]
                tile_price = self.get_price(tile=tile)
                tile_area = tile[0] * tile[1]
                total_area = rem_surface

                if self.tile_is_possible(tile=tile, cost_tile=tile_price, total_cost=total_cost,
                                         rem_surface=rem_surface):

                    for configs in config:

                        if self.can_place_tile(x=position[0], y=position[1], tile=configs, partial_solution=solution):
                            res_postions = self.add_tile_to_solution(x=position[0], y=position[1], tile=configs, pos=solution,
                                                            partial_solution=solution)


                            new_pos = pos.add(res_postions)
                            rem_surface = total_area - tile_area
                            rem_tiles.remove(tile)
                            total_cost = total_cost + tile_price
                            solution[position] = configs

                            if rem_surface == 0:
                                return (solution, total_cost)
                            else:
                                self.recursive_search(pos=new_pos, rem_surface=rem_surface, rem_tiles=rem_tiles,
                                                  solution=solution, total_cost=total_cost)

        return None

        print(solution)
        print(rem_surface)

        raise NotImplementedError()

    def start_search(self):
        """
        Function that starts the search for a tiling pattern that fills the given area
        using the tiles in the inventory of Tegelaar. 
        The backtracking itself is performed by _recursive_search, which will call itself
        recursively.  

        If you encounter a schedule that you already know to be invalid, you
        should backtrack and try another option.
        This function can be implemented by a single call to another function,
        _build_schedule_recursive. You are allowed to change the arguments of
        the function _build_schedule_recursive

        :return: a tuple (tiling pattern, total cost) if a valid tiling pattern exists 
                 within the budget, otherwise None
                 Note: a valid tiling pattern as a dictionary mapping the bottom left corners
                 of tiles to the tiles used (width, height)
        """
        return self.recursive_search(pos=set([(0, 0)]), rem_surface=self.area, rem_tiles=deepcopy(self.tiles),
                                     solution=dict(), total_cost=0)


def visualize_solution(width: float, height: float,
                       solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]]):
    """
    Function that visualizes a solution on a rectangular surface of width x height

    :param width: The width of the surface
    :param height: The height of the surface
    :param solution: The solution we want to visualize
    """
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html
    if solution is None:
        print("Solution was None -> could not visualize")
        return

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots()
    for (x, y), (w, h) in solution.items():
        ax.add_patch(Rectangle((x, y), w, h, edgecolor='black'))

    plt.ylim(0, max(width, height))
    plt.xlim(0, max(width, height))
    plt.show()
