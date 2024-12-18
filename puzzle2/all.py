"""
This program solves both parts of Day 2 puzzle.
"""

from aoc import *

type report = list[int]


def is_safe_with_dampener(r: report) -> bool:
    """
    Determines whether report r is safe, using the Problem Dampener.
    """
    if is_safe(r):
        return True
    for i in range(len(r)):
        r1 = r[:]
        del r1[i]
        if is_safe(r1):
            return True
    return False


def is_safe(r: report) -> bool:
    """
    Determines whether report r is safe, without the use of the Problem Dampener.
    """
    is_increasing = 1 if r[1] - r[0] > 0 else -1
    for i in range(len(r)-1):
        gap = (r[i+1] - r[i]) * is_increasing
        if gap < 1 or gap > 3:
            return False
    return True


def parse_input(content: file_content) -> list[report]:
    """
    Parse the input as a list of reports.
    """
    return [list(map(int, line.split())) for line in content]


def main():
    content = readfile("input")
    data = parse_input(content)
    count = 0
    count_dampener = 0
    for report in data:
        count += is_safe(report)
        count_dampener += is_safe_with_dampener(report)
    print("part 1:", count)
    print("part 2:", count_dampener)


main()
