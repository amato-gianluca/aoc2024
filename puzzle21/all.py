"""
This program solves both parts of the Day 21 puzzle.
"""

import functools

from aoc import *

type keypad = dict[str, tuple[int, int]]

NUMERIC_KEYPAD: keypad = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "X": (0, 3),
    "0": (1, 3),
    "A": (2, 3)
}

DIRECTIONAL_KEYPAD: keypad = {
    "X": (0, 0),
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}


def keyboard_command(code: str, n: int) -> int:
    """
    Return the number of keys needed to type the numeric code `code` with `n`
    robots in the middle.
    """
    moves = 0
    x_bad, y_bad = NUMERIC_KEYPAD["X"]
    x, y = NUMERIC_KEYPAD["A"]
    for button in code:
        x_new, y_new = NUMERIC_KEYPAD[button]
        x_diff = ">" * (x_new - x) if x_new >= x else "<" * (x - x_new)
        y_diff = "v" * (y_new - y) if y_new >= y else "^" * (y - y_new)
        attempts: list[int] = []
        if not (x_new == x_bad and y == y_bad):
            attempts.append(direction_command(x_diff + y_diff + "A", n))
        if not (y_new == y_bad and x == x_bad):
            attempts.append(direction_command(y_diff + x_diff + "A", n))
        moves += min(attempts)
        x, y = x_new, y_new
    return moves


@functools.cache
def direction_command(code: str, n: int) -> int:
    """
    Return the number of keys needed to type the directional code `code` with `n`
    robots in the middle.
    """
    if n == 0:
        return len(code)
    moves = 0
    x_bad, y_bad = DIRECTIONAL_KEYPAD["X"]
    x, y = DIRECTIONAL_KEYPAD["A"]
    for button in code:
        x_new, y_new = DIRECTIONAL_KEYPAD[button]
        x_diff = ">" * (x_new - x) if x_new >= x else "<" * (x - x_new)
        y_diff = "v" * (y_new - y) if y_new >= y else "^" * (y - y_new)
        attempts: list[int] = []
        if not (x_new == x_bad and y == y_bad):
            attempts.append(direction_command(x_diff + y_diff + "A", n-1))
        if not (y_new == y_bad and x == x_bad):
            attempts.append(direction_command(y_diff + x_diff + "A", n-1))
        moves += min(attempts)
        x, y = x_new, y_new
    return moves


def complexity(code: str, length: int) -> int:
    """
    Return the complexity of numeric code `str` with `n` robots in the midddle.
    """
    length = keyboard_command(code, length)
    num = int(code[:-1])
    return length * num


codes = readfile("input")
part1 = sum(complexity(code, 2) for code in codes)
print("part 1:", part1)

part2 = sum(complexity(code, 25) for code in codes)
print("part 2:", part2)
