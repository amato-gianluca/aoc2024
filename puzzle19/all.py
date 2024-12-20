import functools
from operator import methodcaller
from typing import TextIO

from aoc import *


def read_towels(f: TextIO) -> list[str]:
    """
    Read list of available towels.
    """
    return list(map(methodcaller("strip"), f.readline().split(",")))


def read_designs(f: TextIO) -> list[str]:
    """
    Read list of desired designs.
    """
    return f.read().splitlines()


def reachable(design: str, towels: list[str]) -> int:
    """
    Return the number of ways it is possible to produce the design with the
    given set of towels.
    """

    @functools.cache
    def reachable_pattern(start: int) -> int:
        if start == len(design):
            return 1
        count = 0
        for pattern in towels:
            plen = len(pattern)
            if design[start:start+plen] == pattern:
                count += reachable_pattern(start+plen)
        return count

    return reachable_pattern(0)


def main():
    with openfile("input") as f:
        towels = read_towels(f)
        f.readline()
        designs = read_designs(f)
    reachables = [reachable(pattern, towels) for pattern in designs]
    print("part 1:", sum(map(bool, reachables)))
    print("part 2:", sum(reachables))


main()
