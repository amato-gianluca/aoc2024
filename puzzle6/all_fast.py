"""
This program solves both parts of the Day 6 puzzle.

This uses less abstractions and is faster of the other solution.
"""

import time

type vector2d = tuple[int, int]
type visited_list = list[list[list[vector2d]]]


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
        self.visited: visited_list = [
            [[] for _ in range(self.num_cols)] for _ in range(self.num_rows)
        ]
        self.obstacles: set[vector2d] = set()
        self.clear()

    def clear(self):
        """
        Reset the guard at the initial state. Only resets additinal obstacles.
        """
        self.i, self.j = self.starting_position
        self.direction: vector2d = -1, 0
        for row in self.visited:
            for s in row:
                s.clear()
        self.visited[self.i][self.j].append(self.direction)
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
                return i, j
        # default guard position
        return 0, 0

    def step(self) -> str:
        """
        Execute a step action of the guard. Rotation counts as a step.
        """
        i = self.i + self.direction[0]
        j = self.j + self.direction[1]
        if 0 <= i < self.num_rows and 0 <= j < self.num_cols:
            if self.map[i][j] == "#" or (i, j) in self.obstacles:
                self.direction = self.direction[1], - self.direction[0]
                i = self.i
                j = self.j
            else:
                self.i = i
                self.j = j
            current_directions = self.visited[i][j]
            if self.direction in current_directions:
                return 'loop'
            else:
                current_directions.append(self.direction)
                return 'normal'
        else:
            return 'exit'

    def count_visited(self) -> int:
        """
        Return the number of cells visited by the guard.
        """
        return sum(len(pos) > 0 for row in self.visited for pos in row)

    def run(self) -> str:
        """
        Executes steps until the guard exits from the map or a loop is detected.
        """
        while (ret := self.step()) == 'normal':
            pass
        return ret


def loop_detect(g: guard, obs: vector2d) -> bool:
    """
    Return whether a loop is caused by adding an obstacle at given position.
    """
    g.clear()
    g.add_obstacle(obs)
    return g.run() == "loop"


def find_loops(g: guard) -> int:
    """
    Return the number of positions where an obstacle might cause a loop.
    """
    is_visited = [[bool(s) for s in row] for row in g.visited]
    num_loops = 0
    for i in range(g.num_rows):
        for j in range(g.num_cols):
            obstacle = i, j
            if obstacle != g.starting_position and is_visited[i][j]:
                num_loops += loop_detect(g, obstacle)
    return num_loops


def read_map(filename: str) -> list[str]:
    """
    Read the map from the given file.
    """
    with open(filename) as f:
        return [line.rstrip() for line in f]


def main():
    g = guard(read_map("puzzle6/input"))
    g.run()
    print("part 1:", g.count_visited())
    print("part 2:", find_loops(g))


# import cProfile
# cProfile.run('main()')
start_time = time.time()
main()
print(f"--- {(time.time() - start_time)} seconds ---")
