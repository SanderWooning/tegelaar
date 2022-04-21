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

        :return a rotated tile (height_tile, width_tile)
        """
        return tuple([tile[1], tile[0]])

    def get_price(self, tile: typing.Tuple[float, float]):
        """
        Looks up and returns the price of the given tile.

        Steps:
            1. Check if the tile is in prices dict. and return it's price.
            2. Check if the rotated tile is in the prices dict. and return it's price.

        :param tile: a tile (width_tile, height_tile)

        :returns the price of a tile.
        """

        if tile in self.prices:
            return self.prices[tile]

        # Check for rotated tile.
        if self.rotate_tile(tile) in self.prices:
            tile = self.rotate_tile(tile)
            return self.prices[tile]

    def tile_is_possible(self, tile: typing.Tuple[float, float], cost_tile: float,
                         total_cost: float, rem_surface: float):

        """
        Function that checks whether the tile can be used based on
           - whether there is enough budget left
           - whether there is enough remaining surface to potentially hold a place for the tile

        Steps:
            1. Check if the remaining surface after placing the tiles is not a negative number.
            2. Check if the total cost after placing the tile does not exceeds the budget.

        :param tile: The tile (tile_width, tile_height)
        :param cost_tile: The cost of the tile
        :param total_cost: The total cost of the current partial solution
        :param rem_surface: The surface that we yet have to fill

        :returns True if the tile can be potentially placed (enough budget and remaining surface)
        and False otherwise
        """

        # If rem_surface - tile_area is negative, there is no place for the tile.
        if rem_surface - (tile[0] * tile[1]) < 0:
            return False

        # Budget check
        if cost_tile + total_cost > self.budget:
            return False

        else:
            return True

    @staticmethod
    def tiles_overlap(pos1: typing.Tuple[float, float], tile1: typing.Tuple[float, float],
                      pos2: typing.Tuple[float, float], tile2: typing.Tuple[float, float]):

        """
        Function that checks whether two tiles are overlapping

        Steps:
            1. Check if any positions do not overlap.
                a. Firstly check if any positions are on the same line by checking if any square are equal.
                b. Then check if any rectangle is on the left side
                c. Check if rectangle is above the other one.
            2. Any remaining positions will always overlap.

        :param pos1: the bottom-left corner (x1, y1) where tile1 starts
        :param tile1: (width_tile1, height_tile1)
        :param pos2: the bottom-left corner (x2, y2) where tile2 starts
        :param tile2: (width_tile2, height_tile2)

        :return True when the two tiles are overlapping. False otherwise
        """

        # Check for non-overlapping positions.
        if (pos1[0] >= (pos2[0] + tile2[0])) or \
                ((pos1[0] + tile1[0]) <= pos2[0]) or \
                ((pos1[1] + tile1[1]) <= pos2[1]) or \
                (pos1[1] >= (pos2[1] + tile2[1])):
            return False

        # Any other squares do overlap.
        else:
            return True

    def has_overlap(self, position: typing.Tuple[float, float], tile: typing.Tuple[float, float],
                    solution: typing.Dict[typing.Tuple[float, float], typing.Tuple[float, float]]):

        """
        Function that checks whether the tile overlaps with other tiles in the solution
        if it would be placed on the given position

        :param position: the (x,y) coordinate pair where the tile is to be placed
        :param tile: the tile (width_tile1, height_tile1)
        :param solution: the current solution (dictionary mapping positions (x,y)->(tile_width, tile_height))

        :return True if there is overlap between the tile on position and the other tiles in the solution
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

        :return True if the tile can be placed (does not violate mentioned constraints)
        and False otherwise
        """

        # Out-of-bounds check
        if x + tile[0] > self.width or y + tile[1] > self.height:
            return False

        # Overlap check
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

        :return a list of new positions (x', y') that were added to pos. Importantly, new means that
        they were not present before in pos.
        """
        new_positions = []

        partial_solution[(x, y)] = tile

        right_corner = (x + tile[0], y)
        if right_corner not in pos:
            new_positions.append(right_corner)

        top_corner = (x, y + tile[1])
        if top_corner not in pos:
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

        Steps:
            1. Check the positive and negative-basecase (if the remaining surface is 0, which means the area is filled,
                then return the tiling_solution). Or if there are no tiles are remaining, there is no solution.
            2. Iterate over all positions.
            3. Iterate over all tiles in that position
            4. Get tile information and it's possible rotations
            5. Check if the tile is possible
            6. Iterate over all tile configurations (The normal tile and the rotated tile)
            7. Check if the tile overlaps with any current tiles in the partial_solution.
            8. Place tile
            9. Different functions for updating tile-area parameters such a total_cost, positions,
            10. Call function again (recursion)
            11. Check if updated parameters result in a tiling solution. no result has been found, call function again (recurssion)
            11. If not, undo actions by updating tile-area parameters to previous values.

        :param pos: The set of bottom left corners on which we can potentially put tiles 
                    (initially only (0,0) ~ start filling the area from the bottom left)
        :param rem_surface: the remaining surface to be filled
        :param rem_tiles: the remaining tiles that are in the inventory
        :param solution: the partial solution (same structure as pos)
        :param total_cost: the total cost of the partial solution

        :return a tuple (tiling pattern, total cost) if a valid tiling pattern exists
                 within the budget, otherwise return None, None
        """

        # Positive base-case.
        if rem_surface == 0:
            return solution, total_cost

        # Negative base-case for efficiency
        if len(rem_tiles) == 0:
            return None, None

        # Add copy to make sure pos is not being altered within the function itself.
        initial_pos = deepcopy(pos)

        # Iterate over all available positions and try every tile in every configuration.
        for position in initial_pos:
            for tile in rem_tiles:

                # Obtain certain parameters of the tile such as configurations (possible rotations), price and area.
                configs = [tile, self.rotate_tile(tile)]
                tile_price = self.get_price(tile=tile)
                tile_area = tile[0] * tile[1]

                # Check if the tile itself is possible. If not continue.
                if self.tile_is_possible(tile=tile, cost_tile=tile_price, total_cost=total_cost,
                                         rem_surface=rem_surface):

                    # Iterate over all configurations of the tile
                    for config in configs:

                        # Check if the configuration of the tile has any overlap.
                        if self.can_place_tile(x=position[0], y=position[1], tile=config, partial_solution=solution):

                            # Place tile itself and the get next positions
                            res_postions = self.add_tile_to_solution(x=position[0], y=position[1], tile=config,
                                                                     pos=pos, partial_solution=solution)

                            # Remove the used position and add the new positions to the list.
                            pos.remove(position)
                            for i in res_postions:
                                pos.add(i)

                            # Update parameters like remaining surface,
                            # remaining tiles and the current cost of the tiling-solution
                            rem_surface = rem_surface - tile_area
                            rem_tiles.remove(tile)
                            total_cost = total_cost + tile_price

                            possible_solution = self.recursive_search(pos=pos, rem_surface=rem_surface,
                                                                      rem_tiles=rem_tiles,
                                                                      solution=solution, total_cost=total_cost)

                            # If a solution if found, return it to the parent. Which results in the parent return it
                            # again and therefore ending up at the top node and returning.

                            if possible_solution != (None, None):
                                return possible_solution

                            # Return certain parameters such as the placed tile,
                            # the rem_surface, rem_tiles and total-cost.
                            pos.add(position)
                            rem_surface = rem_surface + tile_area
                            rem_tiles.append(tile)
                            total_cost = total_cost - tile_price
                            del solution[position]

        return None, None

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
                 within the budget, otherwise return None, None

                 Note: a valid tiling pattern as a dictionary mapping the bottom left corners
                 of tiles to the tiles used (width, height)
        """

        # A initial check for efficiency. This code checks if all tiles in the inventory have the ability to cover
        # the wanted area. This is done by iteration over all tiles and calculating their area together.
        # If the total_tile_area is smaller then self.area, there will never be a solution thus returning None, None

        total_tile_area = 0
        for tile in deepcopy(self.tiles):
            total_tile_area += tile[0] * tile[1]

        if total_tile_area < self.area:
            return None, None

        else:
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
