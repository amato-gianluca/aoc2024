"""
This program solves part 1 of the Day 14 puzzle.
"""

import re
import math
from typing import NamedTuple, TextIO


SIZE_X = 101
SIZE_Y = 103
TIME_STEPS = 100

class robot(NamedTuple):
    posx: int
    posy: int
    vx: int
    vy: int

    def time_lapse(self, steps: int) -> tuple[int, int]:
        return (self.posx + steps * self.vx) % SIZE_X,  (self.posy + steps * self.vy) % SIZE_Y


def read_robot(f: TextIO) -> robot | None:
    line = f. readline()
    if line == "":
        return None
    data, = re.findall(r"p=([-]?\d+),([-]?\d+) v=([-]?\d+),([-]?\d+)", line)
    return robot(*map(int, data))

def quadrant(x: int, y: int) -> int | None:
    if x == SIZE_X // 2 or y == SIZE_Y // 2:
        return None
    else:
        return 2*(y < SIZE_Y // 2) + (x < SIZE_X // 2)

with open("puzzle14/input") as f:
    quadrants = [0] * 4
    while r := read_robot(f):
        x, y = r.time_lapse(TIME_STEPS)
        if ((q := quadrant(x, y)) is not None):
            quadrants[q] += 1
print("part 1:", math.prod(quadrants))
