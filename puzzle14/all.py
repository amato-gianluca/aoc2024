"""
This program solves both parts of the Day 14 puzzle.
"""

import re
import math
from typing import Generator
from dataclasses import dataclass

# SIZE_X = 11
# SIZE_Y= 7

SIZE_X = 101
SIZE_Y = 103
TIME_STEPS = 100

@dataclass
class robot:
    """
    A class representing a robot.
    """
    posx: int
    posy: int
    vx: int
    vy: int

    def step(self):
        """
        Single step evolution of the robot.
        """
        self.posx = (self.posx + self.vx) % SIZE_X
        self.posy = (self.posy + self.vy) % SIZE_Y

    def quadrant(self) -> int | None:
        """
        Return the quadrant of the current robot (from 0 to 3) or None if the robot
        is out of any quadrant.
        """
        if self.posx == SIZE_X // 2 or self.posy == SIZE_Y // 2:
            return None
        else:
            return 2*(self.posy < SIZE_Y // 2) + (self.posx < SIZE_X // 2)


class bathroom:
    """
    A class representing the entrie room of robots.
    """
    def __init__(self, robots: list[robot]):
        """
        Initialize the room with the given list of robots.
        """
        self.robots = robots

    def step(self):
        """
        Single step evolution of all robots.
        """
        for r in robots:
            r.step()

    def safety_factor(self) -> int:
        """
        Compute the safety factor of the current robot disposition.
        """
        quadrants = [0] * 4
        for r in robots:
            if ((q := r.quadrant()) is not None):
                quadrants[q] += 1
        return math.prod(quadrants)

    def __str__(self) -> str:
        s = [[" "] * SIZE_X for _ in range(SIZE_Y)]
        for r in self.robots:
            s[r.posy][r.posx] = "*"
        return "\n".join(["".join(line) for line in s])

    def is_christmas_tree(self) -> bool:
        """
        Return whether the robots form a Christmas tree.
        """
        star_line = "*" * (SIZE_X // 4)
        return str(self).find(star_line) != -1


def read_robots(filename: str) -> Generator[robot, None, None]:
    """
    A generator yield the robots encoded in the given file.
    """
    with open(filename) as f:
        for line in f:
            if line == "":
                break
            data, = re.findall(r"p=([-]?\d+),([-]?\d+) v=([-]?\d+),([-]?\d+)", line)
            yield robot(*map(int, data))


robots = [ r for r in read_robots("puzzle14/input") ]
br = bathroom(robots)
time: int = 0
tree_time = None
safety_factor = None
while time <= 100 or tree_time is None:
    if br.is_christmas_tree() and tree_time is None:
        tree_time = time
    if time == 100:
        safety_factor = br.safety_factor()
    br.step()
    time += 1

print("part 1:", safety_factor)
print("part 2:", tree_time)
