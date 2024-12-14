"""
This program solves both parts of the Day 13 puzzle.
"""

from typing import NamedTuple, Generator
import re

COSTA = 3
COSTB = 1

INCREASE = 10000000000000


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


def read_machines(filename: str) -> Generator[machine, None, None]:
    """
    Generator which reads machines from the given file.
    """
    with open(filename) as f:
        while True:
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

            # skip empty line
            f.readline()

            yield machine(ax, ay, bx, by, posx, posy)


def solve_machine(m: machine) -> int | None:
    """
    Return the minimum cost for winning a prize with the given machine, None if
    it is not possible to win.

    This works by solving  a system of 2 linear equation in 2 unknowns, and checking
    if the solution is integer.
    """
    num = m.ax * m.posy - m.posx * m.ay
    den = m.ax * m.by - m.bx * m.ay
    if den == 0 and num != 0:
        return None
    # the program does not handle the indeterminate case when both num and den are 0
    if num % den == 0:
        j = num // den
        num = m.posx - j * m.bx
        den = m.ax
        if num % den == 0:
            i = num // den
            return i * COSTA + j * COSTB
    return None


cost1 = cost2 = 0
for m1 in read_machines("puzzle13/input"):
    if cost := solve_machine(m1):
        cost1 += cost
    m2 = m1._replace(posx=m1.posx + INCREASE, posy=m1.posy + INCREASE)
    if cost := solve_machine(m2):
        cost2 += cost

print("part 1:", cost1)
print("part 2:", cost2)
