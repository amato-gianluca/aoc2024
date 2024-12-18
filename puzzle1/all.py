"""
This program solves both parts of Day 1 puzzle.
"""

from collections import Counter
from typing import Iterable

from aoc import *


def parse_input(content: file_content):
    """
    Convert the file content into a pair of iterables.
    """
    l = (map(int, line.split()) for line in content)
    return zip(*l)


def distance(l1: Iterable[int], l2: Iterable[int]) -> int:
    """
    Return the Manhattan distance of the two iterables.
    """
    return sum(abs(a-b) for a, b in zip(sorted(l1), sorted(l2)))


def similarity(l1: Iterable[int], l2: Iterable[int]) -> int:
    """
    Return the similarity score of the two iterables.
    """
    d: Counter[int] = Counter(l2)
    return sum(x*d[x] for x in l1)


def main():
    content = readfile("example")
    l1, l2 = parse_input(content)
    print("part 1:", distance(l1, l2))
    print("part 2:", similarity(l1, l2))


main()
