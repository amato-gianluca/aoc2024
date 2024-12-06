"""
This program solves both parts of the Day 5 puzzle.

It implements a minimal multi-dict class.
"""

from collections import defaultdict
from functools import cmp_to_key
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
    count1 = 0
    count2 = 0
    for line in file:
        sequence = [int(x) for x in line.rstrip().split(",")]
        if all(constraints.check(*s) for s in pairwise(sequence)):
            count1 += sequence[len(sequence)//2]
        else:
            def comparison_function(a: int, b: int):
                return 0 if a == b else -1 if constraints.check(a, b) else 1
            sequence.sort(key=cmp_to_key(comparison_function))
            count2 += sequence[len(sequence)//2]
    return count1, count2


with open("puzzle5/input") as file:
    constraints = read_constraints(file)
    count1, count2 = check_constraints(file, constraints)

print("part 1:", count1)
print("part 2:", count2)
