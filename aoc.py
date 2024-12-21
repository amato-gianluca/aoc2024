"""
A module with utilty classes and functions for AoC.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path
from typing import Callable, Iterable, TextIO

import __main__

type file_content = list[str]


def readfile(filename: str) -> file_content:
    """
    Read an entire file.
    """
    with open(str(Path(__main__.__file__).parent / filename)) as f:
        return f.read().splitlines()


def openfile(filename: str) -> TextIO:
    """
    Open a file in the correct directory.
    """
    return open(str(Path(__main__.__file__).parent / filename))


class multidict[K, V]:
    def __init__(self):
        """
        Initialize the multi dictionary.
        """
        self._dict: dict[K, set[V]] = defaultdict(set)

    def add(self, key: K, value: V):
        """
        Add value V to key K.
        """
        self._dict[key].add(value)

    def check(self, key: K, value: V) -> bool:
        """
        Check if V is associated to K
        """
        return value in self._dict[key]


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

    def pop(self) -> V | None:
        """
        Extract the element with lowest priority.
        """
        while self.heap:
            entry = heappop(self.heap)
            if entry.value is not None:
                del self.entry_finder[entry.value]
                return entry.value
        return None


class Dijkstra[V]:
    """
    A class representing the set of shortests path in a graph from a given starting node, computed
    using the Dijkstra algorithm.
    """

    def __init__(self, start: V, moves: Callable[[V], Iterable[tuple[V, int]]]):
        """
        Execute the Dijkstra algorithm.

        Parameters:
        - `start` is the start node
        - `moves` returns, for each node src, a list of pairs (dst, w) such that dst is reachable from src with weight w
        Returns:
        - a map from a node to all the predecessors in the shortest paths from start.
        - a map from a node n to the shortest distance from start to n.
        """
        self.start = start
        self.moves = moves
        self.prevs, self.dists = self.__dijkstra__(start, moves)

    @staticmethod
    def __dijkstra__(start: V, moves: Callable[[V], Iterable[tuple[V, int]]]) -> tuple[dict[V, list[V]], dict[V, int]]:
        """
        Actually perform the algorithm.
        """
        pq = priority_queue[V]()
        distance: dict[V, int] = {}
        prev: dict[V, list[V]] = defaultdict(list)

        distance[start] = 0
        prev[start] = [start]
        pq.add(start, 0)
        while True:
            node = pq.pop()
            if node is None:
                return prev, distance
            dist = distance[node]
            for node_new, cost in moves(node):
                dist_update = dist + cost
                if node_new in distance:
                    dist_new = distance[node_new]
                    if dist_update < dist_new:
                        pq.add(node_new, dist_update)
                        distance[node_new] = dist_update
                        prev[node_new] = [node]
                    elif dist_update == dist_new:
                        prev[node_new].append(node)

                else:
                    distance[node_new] = dist_update
                    pq.add(node_new, dist_update)
                    prev[node_new] = [node]

    def path_compute(self, end: V) -> list[V] | None:
        """
        Return one of the shortest paths leading to `end`, or None is such a path does not exist.
        """
        if end not in self.prevs:
            return None
        current = end
        path = [current]
        while (p := self.prevs[current][0]) != current:
            path.append(p)
            current = p
        path.reverse()
        return path

    def nodes_in_path(self, end: V) -> set[V]:
        """
        Return the set of all nodes in the shortest paths leading to end.
        """
        nodes: set[V] = {end}
        for prev in self.prevs[end]:
            if prev != end:
                nodes.update(self.nodes_in_path(prev))
        return nodes


class Maze:
    """
    Class modeling a maze.
    """

    type position = tuple[int, int]

    def __init__(self, map: list[str]):
        """
        Initialize the maze from the map given as a list of strings.
        """
        self.map = map
        self.i_start, self.j_start = self._find_char(self.map, "S")
        self.i_end, self.j_end = self._find_char(self.map, "E")
        self.nrow = len(self.map)
        self.ncol = len(self.map[0])

    @staticmethod
    def _find_char(map: list[str], ch: str) -> position:
        """
        Return the position of a given character in a list of strings.
        """
        return [(i, j)
                for i, line in enumerate(map)
                for j, obj in enumerate(line)
                if obj == ch][0]

    def adjacent_positions(self, pos: position) -> list[position]:
        """
        Return the list of positions reachable from `pos`.
        """
        i, j = pos
        choices = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        return [
            (i_new, j_new)
            for i_new, j_new in choices
            if self.map[i_new][j_new] != "#" and 0 <= i_new < self.nrow and 0 <= j_new < self.ncol
        ]

    def dijkstra(self, start: position | None = None) -> Dijkstra[position]:
        """
        Apply Dijikstra shortes path algorith to the maze, with the given starting node (by default,
        it is the starting node of the maze).
        """
        if start is None:
            start = (self.i_start, self.j_start)
        moves: Callable[[Maze.position], list[tuple[Maze.position, int]]] = lambda pos: [
            (pos_new, 1) for pos_new in self.adjacent_positions(pos)]
        return Dijkstra(start, moves)

    def __str__(self):
        return "\n".join("".join(line) for line in self.map)
