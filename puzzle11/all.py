"""
This program solves both parts of the Day 11 puzzle.
"""

import functools

from aoc import *


@functools.cache
def blink(x: int, n: int) -> int:
    """
    Blink a single stone x for n times, and return the final number of stones.
    """
    if n == 0:
        return 1
    elif x == 0:
        return blink(1, n-1)
    elif (sizex := len(str(x))) % 2 == 0:
        pow = 10 ** (sizex // 2)
        return blink(x // pow, n - 1) + blink(x % pow, n - 1)
    else:
        return blink(x * 2024, n-1)


def blink_line(l: list[int], n: int) -> int:
    """
    Blink the line l for n times, and return the final the number of stones.
    """
    return sum(blink(v, n) for v in l)


def parse_line(line: str) -> list[int]:
    """
    Parse the input line.
    """
    return list(map(int, line.split()))


def main():
    content = readfile("input")
    l = parse_line(content[0])
    print("part 1:", blink_line(l, 25))
    print("part 2:", blink_line(l, 75))
    print(blink.cache_info())


main()
