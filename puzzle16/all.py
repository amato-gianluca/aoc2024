"""
This program solves both parts of the Day 16 puzzle.
"""

from typing import NamedTuple
from enum import Enum
from dataclasses import dataclass, field
from heapq import heappush, heappop

INFINITY = 10000000
"""This should be larger than the minimum path between start and end cell."""


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


class Node(NamedTuple):
    """
    The combination of positions in the maze and orientation for the raindeer.
    """
    i: int
    j: int
    dir: Direction


class priority_queue[V]:
    """
    A priority queue for elements of type V. Its implementation in terms of heaps is
    taken from the online Python reference manual.
    """

    @dataclass(order=True)
    class _Entry:
        """
        An entry containing a value and a priority. The entry is ordered according
        to priority.
        """
        value: V | None = field(compare=False)
        priority: int

    def __init__(self):
        """
        Initialize an empty priority queue.
        """
        self.entry_finder: dict[V, priority_queue._Entry] = {}
        self.heap: list[priority_queue._Entry] = []

    def add(self, value: V, priority: int):
        """
        Add an element to the priority queue or update its priority.
        """
        if value in self.entry_finder:
            entry = self.entry_finder[value]
            entry.value = None
        entry = priority_queue._Entry(value, priority)
        self.entry_finder[value] = entry
        heappush(self.heap, entry)

    def pop(self) -> V:
        """
        Extract the element with lowest priority.
        """
        while self.heap:
            entry = heappop(self.heap)
            if entry.value is not None:
                del self.entry_finder[entry.value]
                return entry.value
        raise ValueError("Empty priority queue")


class maze:
    """
    Implementation of the maze and the shortest path algorithm.
    """

    def __init__(self, map: list[str]):
        """
        Initialize the object from the map given as a list of strings.
        """
        self.map = map
        self.i_start, self.j_start = self._find_char(self.map, "S")
        self.i_end, self.j_end = self._find_char(self.map, "E")
        self.nrow = len(self.map)
        self.ncol = len(self.map[0])

    @staticmethod
    def _find_char(map: list[str], ch: str) -> tuple[int, int]:
        """
        Return the position of a given character in a list of strings.
        """
        return [(i, j)
                for i, line in enumerate(map)
                for j, obj in enumerate(line)
                if obj == ch][0]

    def shortest_path(self):
        """
        Return the cost of the shortest past from the starting to the ending position.
        """
        pq = priority_queue[Node]()
        distance: dict[Node, int] = {}
        prev: list[list[set[tuple[int, int]]]] = [
            [set() for _ in range(self.ncol)] for _ in range(self.nrow)
        ]

        # Add all empty cells in the maze to the priority queue and set their distance
        # to infinity.
        for i in range(self.nrow):
            for j in range(self.ncol):
                for dir in Direction:
                    if self.map[i][j] != "#":
                        node = Node(i, j, dir)
                        distance[node] = INFINITY
                        pq.add(node, INFINITY)

        # Change distance of the starting node to 0.
        start_node = Node(self.i_start, self.i_end, Direction.RIGHT)
        distance[start_node] = 0
        pq.add(start_node, 0)
        prev[self.i_start][self.i_end] = {(self.i_start, self.i_end)}
        while True:
            node = pq.pop()
            i, j, dir = node
            dist = distance[node]
            if i == self.i_end and j == self.j_end:
                return dist, len(prev[i][j])
            di, dj = dir.delta()
            moves = [(i + di, j + dj, dir, 1),
                     (i, j, dir.rotate_clockwise(), 1000),
                     (i, j, dir.rotate_counterclockwise(), 1000)]
            for i_new, j_new, dir_new, cost in moves:
                if self.map[i_new][j_new] != "#":
                    node_new = Node(i_new, j_new, dir_new)
                    dist_new = distance[node_new]
                    dist_update = dist + cost
                    if dist_update < dist_new:
                        pq.add(node_new, dist_update)
                        distance[node_new] = dist_update
                        prev[i_new][j_new] = prev[i][j].union({(i_new, j_new)})
                    elif dist_update == dist_new:
                        prev[i_new][j_new] |= prev[i][j]

    def __str__(self):
        return "\n".join("".join(line) for line in self.map)


def read_file(filename: str) -> list[str]:
    """
    Return the content of file `filename` as a list of strings.
    """
    with open(filename) as f:
        return f.read().splitlines()


m_map = read_file("puzzle16/input")
m = maze(m_map)

cost, prevs = m.shortest_path()
print("part 1:", cost)
print("part 2:", prevs)
