"""
This program solves both parts of the Day 5 puzzle.

It implements a minimal multi-dict class and builds a dynamically
defined class which extends int with a new ordering.
"""

from collections import defaultdict
from itertools import pairwise
from typing import TextIO


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

    def check(self, key: K, value: V):
        """
        Check if V is associated to K
        """
        return value in self._dict[key]


def int_with_ordering(name: str, constraints: multidict[int, int]):
    """
    Return a class extending int and whose ordering is given by the `constraints` parameter.
    """
    return type(name, (int, ), {
        "__lt__": lambda a, b: constraints.check(a, b),
        # the following is not needed for this application but included for completeness
        "__lte__": lambda a, b: a == b or constraints.check(a, b),
        "__gt__": lambda a, b: constraints.check(b, a),
        "__gt__": lambda a, b: a == b or constraints.check(b, a),
    })


def read_constraints(file: TextIO) -> multidict[int, int]:
    """
    Read the page ordering from the specified file.
    """
    constraints = multidict()
    while (line := file.readline().rstrip()) != "":
        constraints.add(*map(int, line.split("|")))
    return constraints


def check_constraints(file: TextIO, constraints: multidict[int, int]) -> tuple[int, int]:
    """
    Check that sequences read from `file` satisfy `constraints`.
    """
    page = int_with_ordering("page", constraints)
    count1 = 0
    count2 = 0
    for line in file:
        sequence = [page(int(x)) for x in line.rstrip().split(",")]
        if all(constraints.check(*s) for s in pairwise(sequence)):
            count1 += sequence[len(sequence)//2]
        else:
            sequence.sort()
            count2 += sequence[len(sequence)//2]
    return count1, count2


with open("puzzle5/input") as file:
    constraints = read_constraints(file)
    count1, count2 = check_constraints(file, constraints)

print("part 1:", count1)
print("part 2:", count2)
