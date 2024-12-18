"""
This program solves both parts of the Day 6 puzzle.

This uses a lot of abstractions and is quite slow.
"""

import time
from enum import Enum, auto
from typing import NamedTuple

from aoc import *


class vector2d(NamedTuple):
    i: int
    j: int

    def add(self, other: 'vector2d') -> 'vector2d':
        """
        Component-wise addiction of two vectors.
        """
        return vector2d(self.i + other.i, self.j + other.j)

    def rotated(self) -> 'vector2d':
        """
        Rotated vector of 90° clockwise.
        """
        return vector2d(self.j, - self.i)


class guard_status(Enum):
    NORMAL = auto()
    EXIT = auto()
    LOOP = auto()


class guard:
    """
    Models a guard moving inside a map.
    """

    def __init__(self, map_data: list[str]):
        """
        Initialize the guard by providing the map in which she will move.
        """
        self.map = map_data
        self.num_rows = len(self.map)
        self.num_cols = len(self.map[0])
        self.starting_position = self._starting_position(self.map)
        self.visited: list[list[list[vector2d]]] = [
            [[] for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]
        self.obstacles: set[vector2d] = set()
        self.clear()

    def clear(self):
        """
        Reset the guard at the initial state. Also resets additinal obstacles.
        """
        i, j = self.position = self.starting_position
        self.direction = vector2d(-1, 0)
        for row in self.visited:
            for s in row:
                s.clear()
        self.visited[i][j].append(self.direction)
        self.obstacles.clear()

    def add_obstacle(self, obs: vector2d):
        """
        Add additional obstacles.
        """
        self.obstacles.add(obs)

    @staticmethod
    def _starting_position(map_data: list[str]) -> vector2d:
        """
        Return the starting position of the guard in the map.
        """
        for i, row in enumerate(map_data):
            if (j := row.find("^")) > 0:
                return vector2d(i, j)
        # default guard position
        return vector2d(0, 0)

    def step(self) -> guard_status:
        """
        Execute a step action of the guard. Rotation counts as a step.
        """
        i, j = newposition = self.position.add(self.direction)
        if 0 <= i < self.num_rows and 0 <= j < self.num_cols:
            if self.map[i][j] == "#" or newposition in self.obstacles:
                self.direction = self.direction.rotated()
                i, j = self.position
            else:
                self.position = newposition
            current_directions = self.visited[i][j]
            if self.direction in current_directions:
                return guard_status.LOOP
            else:
                current_directions.append(self.direction)
                return guard_status.NORMAL
        else:
            return guard_status.EXIT

    def count_visited(self) -> int:
        """
        Return the number of cells visited by the guard.
        """
        return sum(len(pos) > 0 for row in self.visited for pos in row)

    def run(self) -> guard_status:
        """
        Executes steps until the guard exits from the map or a loop is detected.
        """
        while (ret := self.step()) == guard_status.NORMAL:
            pass
        return ret


def loop_detect(g: guard, obs: vector2d) -> bool:
    """
    Return whether a loop is caused by adding an obstacle at given position.
    """
    g.clear()
    g.add_obstacle(obs)
    return g.run() == guard_status.LOOP


def find_loops(g: guard):
    """
    Return the number of positions where an obstacle might cause a loop.
    """
    is_visited = [[bool(s) for s in row] for row in g.visited]
    num_loops = 0
    for i in range(g.num_rows):
        for j in range(g.num_cols):
            obstacle = vector2d(i, j)
            if obstacle != g.starting_position and is_visited[i][j]:
                num_loops += loop_detect(g, obstacle)
    return num_loops


def main():
    content = readfile("input")
    g = guard(content)
    g.run()
    print("part 1:", g.count_visited())
    print("part 2:", find_loops(g))


# import cProfile
# cProfile.run('main()')
start_time = time.time()
main()
print(f"--- {(time.time() - start_time)} seconds ---")
