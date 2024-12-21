"""
This program solves both parts of the Day 18 puzzle.
"""

from aoc import *


class Day18Maze(Maze):
    """
    Implementation of the maze with falling blocks.
    """

    def __init__(self, size: int, drops: list[tuple[int, int]]):
        """
        Initialize the object from the map given as a list of strings.
        """
        self.nrow = self.ncol = size
        self.map = [["."] * size for _ in range(size)]
        self.i_start, self.j_start = 0, 0
        self.i_end, self.j_end = size-1, size - 1
        self.drops = drops

    def set_time(self, t: int):
        for i in range(t):
            j, i = self.drops[i]
            self.map[i][j] = "#"


def parse_input(input: list[str]) -> list[tuple[int, int]]:
    """
    Return the content of file `filename` as a list of strings.
    """
    return [(int(lsplit[0]), int(lsplit[1])) for l in input for lsplit in (l.split(","),)]


def main():
    # data = ("example", 7, 12)
    data = ("input", 71, 1024)

    drops = parse_input(readfile(data[0]))
    m = Day18Maze(data[1], drops)
    m.set_time(data[2])

    cost = m.shortest_path()
    print("part 1:", cost)

    t = data[2] + 1
    while True:
        m.set_time(t)
        cost = m.shortest_path()
        if cost is None:
            break
        t += 1
    print("part 2:",  drops[t-1])


main()
