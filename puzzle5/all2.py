"""
This program solves both parts of the Day 5 puzzle.

It implements a minimal multi-dict class and builds a dynamically
defined class which extends int with a new ordering.
"""

from itertools import pairwise
from typing import Callable, TextIO

from aoc import *


def int_with_ordering(name: str, constraints: multidict[int, int]):
    """
    Return a class extending int and whose ordering is given by the `constraints` parameter.
    """
    methods: dict[str, Callable[[int, int], bool]] = {
        "__lt__": lambda a, b: constraints.check(a, b),
        # the following is not needed for this application but included for completeness
        "__lte__": lambda a, b: a == b or constraints.check(a, b),
        "__gt__": lambda a, b: constraints.check(b, a),
        "__gt__": lambda a, b: a == b or constraints.check(b, a)
    }
    return type(name, (int, ), methods)


def read_constraints(file: TextIO) -> multidict[int, int]:
    """
    Read the page ordering from the specified file.
    """
    constraints: multidict[int, int] = multidict()
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


def main():
    with openfile("input") as file:
        constraints = read_constraints(file)
        count1, count2 = check_constraints(file, constraints)
    print("part 1:", count1)
    print("part 2:", count2)


main()
