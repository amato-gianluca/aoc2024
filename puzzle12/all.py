"""
This program solves both parts of the Day 12 puzzle.
"""

from typing import NamedTuple

from aoc import *


class region(NamedTuple):
    """
    Represents a region in a garden. Each regions is associated to letter, area, perimeter and number of sides.
    """
    char: str
    area: int
    perimeter: int
    sides: int

    @property
    def cost1(self) -> int:
        """
        The cost of the area according to part 1 of the problem.
        """
        return self.area * self.perimeter

    @property
    def cost2(self) -> int:
        """
        The cost of the area according to part 2 of the problem.
        """
        return self.area * self.sides


class garden:
    """
    A garde, comprised of a map and a sequence of regions.
    """

    def __init__(self, map: list[str]):
        """
        Initialize the garden structure and computes the regions.
        """
        self.map: list[str] = map
        self.nrow: int = len(map)
        self.ncol: int = len(map[0])
        self.regions: list[region] = []
        self._compute_regions()

    def _compute_regions(self):
        """
        Compute the regions of the current map.
        """

        def analyze_cell(i: int, j: int) -> tuple[int, int, int]:
            """
            Computes area, perimeter and sided of the region which contains position (i, j).
            """
            area: int = 1
            perimeter: int = 0
            sides: int = 0
            borders: set[str] = set()
            visited[i][j] = borders
            neighbours = [("up", i-1, j), ("down", i+1, j),
                          ("left", i, j-1), ("right", i, j+1)]

            # Computes the borders of the current cell and add to the perimeter and sides
            for direction, new_i, new_j in neighbours:
                if not (0 <= new_i < self.ncol and 0 <= new_j < self.nrow and self.map[new_i][new_j] == self.map[i][j]):
                    borders.add(direction)
                    perimeter += 1
                    sides += 1

            # If some sides has been already counted in the neighbours, uncount them!
            for direction, new_i, new_j in neighbours:
                if 0 <= new_i < self.ncol and 0 <= new_j < self.nrow and self.map[new_i][new_j] == self.map[i][j] and (neighbour_borders := visited[new_i][new_j]) is not None:
                    sides -= len(borders.intersection(neighbour_borders))

            # Recursively descends on non-visited neighbours of the same region
            for _, new_i, new_j in neighbours:
                if 0 <= new_i < self.ncol and 0 <= new_j < self.nrow and self.map[new_i][new_j] == self.map[i][j] and visited[new_i][new_j] is None:
                    new_area, new_perimeter, new_sides = analyze_cell(
                        new_i, new_j)
                    area += new_area
                    perimeter += new_perimeter
                    sides += new_sides

            # Return results
            return area, perimeter, sides

        visited: list[list[set[str] | None]] = [
            [None] * self.ncol for _ in range(self.nrow)
        ]
        for i in range(self.nrow):
            for j in range(self.ncol):
                if not visited[i][j]:
                    self.regions.append(
                        region(self.map[i][j], *analyze_cell(i, j)))

    def compute_costs(self):
        """
        Compute costs of regions.
        """
        cost1 = cost2 = 0
        for r in self.regions:
            cost1 += r.cost1
            cost2 += r.cost2
        return cost1, cost2


def main():
    m = garden(readfile("input"))
    cost1, cost2 = m.compute_costs()
    print("part 1:", cost1)
    print("part 2:", cost2)


main()
