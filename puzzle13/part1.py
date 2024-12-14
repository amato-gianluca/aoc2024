"""
This program solves part 1 of the Day 13 puzzle with a brute force approach.
"""

from typing import TextIO, NamedTuple
import re

COSTA = 3
COSTB = 1
MAX_STEPS = 100
MAX_COST = (COSTA + COSTB) * 100

class machine(NamedTuple):
    """
    Data for a machine.
    """
    ax: int
    ay: int
    bx: int
    by: int
    posx: int
    posy: int

def read_machine(f: TextIO) -> machine | None:
    """
    Read a single machine from the given file. Returns None if we have
    reached the end of the file.
    """
    line = f.readline()
    if line == "":
        return None
    m = re.match(r".*\+(\d+).*\+(\d+)", line)
    # just to please the type checker
    if m is None:
        return None
    ax, ay = int(m[1]), int(m[2])

    line = f.readline()
    m = re.match(r".*\+(\d+).*\+(\d+)", line)
    # just to please the type checker
    if m is None:
        return None
    bx, by = int(m[1]), int(m[2])

    line = f.readline()
    m = re.match(r".*=(\d+).*=(\d+)", line)
    # just to please the type checker
    if m is None:
        return None
    posx, posy = int(m[1]), int(m[2])

    f.readline()

    return machine(ax, ay, bx, by, posx, posy)

def solve_machine(m: machine) -> int | None:
    """
    Returns the minimum cost for winning a prize with the given machine, None if
    it is not possible to win.
    """
    min_cost = MAX_COST + 1
    i = 0
    while i * m.ax <= m.posx:
        j, mod = divmod(m.posx - i*m.ax, m.bx)
        if mod == 0 and i * m.ay + j * m.by == m.posy:
            cost = COSTA * i + COSTB * j
            min_cost = min(cost, min_cost)
        i += 1
    return min_cost if min_cost < MAX_COST+1 else None

with open("puzzle13/input") as f:
    cost = 0
    while m := read_machine(f):
        if m_cost := solve_machine(m):
            cost +=  m_cost

print("part 1:", cost)
