"""
This program solves part 1 of Day 3 puzzle.
"""

from aoc import *


def parse(s: str):
    """
    Find the mul instructions in `s` and returns the result of the their execution.
    """
    import re
    total = 0
    it = re.finditer(r'mul\(([0-9]+),([0-9]+)\)', s)
    for m in it:
        total += int(m[1]) * int(m[2])
    return total


def main():
    total = 0
    content = readfile("input")
    for line in content:
        total += parse(line)
    print(total)


main()
