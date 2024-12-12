"""
This program solves both parts of the Day 11 puzzle.
"""

import functools

def read_line(filename: str) -> list[int]:
    with open(filename) as f:
        l = list(map(int, f.readline().split()))
    return l

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
    total = 0
    for x in l:
        total += blink(x,  n)
    return total

l = read_line("puzzle11/input")
print("part 1:", blink_line(l, 25))
print("part 2:", blink_line(l, 75))
print(blink.cache_info())