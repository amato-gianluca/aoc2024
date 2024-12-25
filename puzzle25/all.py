"""
This program solves the Day 25 puzzle.
"""

from aoc import *


def parse_key(l: list[str], i: int) -> tuple[bool, list[int], int]:
    """
    Parse a single key or lock, starting at row `i` of the input.

    Returns:
        - a boolean (which is True for locks and False for keys)
        - the key/lock
        - the length of the ley
    """
    res: list[int] = [0] * len(l[i])
    t = l[i][0]
    i += 1
    lenkey = 1
    while i < len(l) and l[i] != "":
        lenkey += 1
        for j in range(len(l[i])):
            if l[i][j] == t:
                res[j] += 1
        i += 1
    return (t == "#", res, lenkey)


def parse_input(content: list[str]) -> tuple[list[list[int]], list[list[int]]]:
    """
    Parse the file content into a list of keys and locks.
    """
    keys: list[list[int]] = []
    locks: list[list[int]] = []
    i = 0
    while i < len(content):
        t, val, lenkey = parse_key(content, i)
        if t:
            locks.append(val)
        else:
            keys.append(val)
        i += lenkey + 1
    return keys, locks

def count_fits(keys: list[list[int]], locks: list[list[int]]) -> int:
    """
    Count the number of keys which fit in locks.
    """
    count = 0
    for l in locks:
        for k in keys:
            if all(lv <= kv for lv, kv in zip(l, k)):
                count += 1
    return count

def main():
    content = readfile("input")
    keys, locks = parse_input(content)
    print("part 1:", count_fits(keys, locks))
    print("part 2: gift!!!")

main()