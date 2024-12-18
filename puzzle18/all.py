"""
This program solves both parts of the Day 18 puzzle.
"""

from typing import NamedTuple

from aoc import *

INFINITY = 10000000
"""This should be larger than the minimum path between start and end cell."""


class Node(NamedTuple):
    """
    The combination of positions in the maze and orientation for the raindeer.
    """
    i: int
    j: int


class maze:
    """
    Implementation of the maze and the shortest path algorithm.
    """

    def __init__(self, size: int, drops: list[tuple[int, int]]):
        """
        Initialize the object from the map given as a list of strings.
        """
        self.nrow = self.ncol = size
        self.map = [["."] * size for _ in range(size)]
        self.drops = drops
        self.i_start, self.j_start = 0, 0
        self.i_end, self.j_end = size-1, size - 1

    def shortest_path(self):
        """
        Return the cost of the shortest past from the starting to the ending position.
        """
        pq = priority_queue[Node]()
        distance: dict[Node, int] = {}

        # Add all empty cells in the maze to the priority queue and set their distance
        # to infinity.
        for i in range(self.nrow):
            for j in range(self.ncol):
                node = Node(i, j)
                distance[node] = INFINITY
                pq.add(node, INFINITY)

        # Change distance of the starting node to 0.
        start_node = Node(self.i_start, self.j_start)
        distance[start_node] = 0
        pq.add(start_node, 0)
        while True:
            node = pq.pop()
            if node is None:
                return INFINITY
            i, j = node
            dist = distance[node]
            if i == self.i_end and j == self.j_end:
                return dist
            moves = [(i, j + 1, 1), (i, j-1, 1), (i+1, j, 1), (i-1, j, 1)]
            for i_new, j_new, cost in moves:
                if 0 <= i_new < self.nrow and 0 <= j_new < self.ncol and self.map[i_new][j_new] != "#":
                    node_new = Node(i_new, j_new)
                    dist_new = distance[node_new]
                    dist_update = dist + cost
                    if dist_update < dist_new:
                        pq.add(node_new, dist_update)
                        distance[node_new] = dist_update

    def set_time(self, t: int):
        for i in range(t):
            j, i = self.drops[i]
            self.map[i][j] = "#"

    def __str__(self):
        return "\n".join("".join(line) for line in self.map)


def parse_input(input: list[str]) -> list[tuple[int, int]]:
    """
    Return the content of file `filename` as a list of strings.
    """
    return [(int(lsplit[0]), int(lsplit[1])) for l in input for lsplit in (l.split(","),)]


def main():
    # data = ("example", 7, 12)
    data = ("input", 71, 1024)

    drops = parse_input(readfile(data[0]))
    m = maze(data[1], drops)
    m.set_time(data[2])

    cost = m.shortest_path()
    print("part 1:", cost)

    t = data[2] + 1
    while True:
        m.set_time(t)
        cost = m.shortest_path()
        if cost == INFINITY:
            break
        t += 1
    print("part 2:",  drops[t-1])


main()
