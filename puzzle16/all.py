"""
This program solves both parts of the Day 16 puzzle.
"""

from enum import Enum

from aoc import *


class Direction(Enum):
    """
    The enumeration of possible directions of the reindeers.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def delta(self) -> tuple[int, int]:
        """
        Return the direction as a tuple of movements on the horizontal and vertical axis.
        """
        match self:
            case Direction.UP:
                return (-1, 0)
            case Direction.DOWN:
                return (1, 0)
            case Direction.RIGHT:
                return (0, 1)
            case Direction.LEFT:
                return (0, -1)

    def rotate_clockwise(self) -> 'Direction':
        """
        Return the direction obtained by rotating clockwise of 90°.
        """
        return Direction((self.value + 1) % len(Direction))

    def rotate_counterclockwise(self) -> 'Direction':
        """
        Return the direction obtained by rotating counterclockwise of 90°.
        """
        return Direction((self.value - 1) % len(Direction))


class Day16Maze(Maze):
    """
    Reindeer maze.
    """

    type pos_with_dir = tuple[int, int, Direction]

    def shortest_path_with_preds(self):
        """
        Return the cost of the shortest paths from the starting to the ending position, and the number
        of nodes in all these shortest paths.
        """

        def moves(pos: Day16Maze.pos_with_dir) -> list[tuple[Day16Maze.pos_with_dir, int]]:
            i, j, dir = pos
            di, dj = dir.delta()
            i_new, j_new = i + di, j + dj
            m = [((i_new, j_new, dir), 1)
                 ] if self.map[i_new][j_new] != "#" else []
            m += [
                ((i, j, dir.rotate_clockwise()), 1000),
                ((i, j, dir.rotate_counterclockwise()), 1000)]
            return m

        start = (self.i_start, self.j_start, Direction.RIGHT)
        ends = [(self.i_end, self.j_end, dir) for dir in Direction]
        dijkstra = Dijkstra(start, moves)
        ends_with_cost = [(end, dijkstra.dists[end]) for end in ends]
        end, cost = min(ends_with_cost, key=lambda x: x[1])
        nodes = {(i, j) for i, j, _ in dijkstra.nodes_in_path(end)}
        return cost, len(nodes)


def main():
    content = readfile("input")
    maze = Day16Maze(content)
    cost, prevs = maze.shortest_path_with_preds()
    print("part 1:", cost)
    print("part 2:", prevs)


main()
