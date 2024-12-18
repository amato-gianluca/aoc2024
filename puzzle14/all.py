"""
This program solves both parts of the Day 14 puzzle.
"""

import math
import re
from dataclasses import dataclass
from typing import Generator

from aoc import *


@dataclass
class robot:
    """
    A class representing a robot.
    """
    posx: int
    posy: int
    vx: int
    vy: int

    def step(self, sizex: int, sizey: int):
        """
        Single step evolution of the robot.
        """
        self.posx = (self.posx + self.vx) % sizex
        self.posy = (self.posy + self.vy) % sizey

    def quadrant(self, sizex: int, sizey: int) -> int | None:
        """
        Return the quadrant of the current robot (from 0 to 3) or None if the robot
        is out of any quadrant.
        """
        if self.posx == sizex // 2 or self.posy == sizey // 2:
            return None
        else:
            return 2*(self.posy < sizey // 2) + (self.posx < sizex // 2)


class bathroom:
    """
    A class representing the entrie room of robots.
    """

    def __init__(self, robots: list[robot], sizex: int, sizey: int):
        """
        Initialize the room with the given list of robots and a given bathroom size.
        """
        self.robots = robots
        self.sizex = sizex
        self.sizey = sizey

    def step(self):
        """
        Single step evolution of all robots.
        """
        for r in self.robots:
            r.step(self.sizex, self.sizey)

    def safety_factor(self) -> int:
        """
        Compute the safety factor of the current robot disposition.
        """
        quadrants = [0] * 4
        for r in self.robots:
            if ((q := r.quadrant(self.sizex, self.sizey)) is not None):
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


def parse_robots(content: file_content) -> Generator[robot, None, None]:
    """
    A generator yield the robots encoded in the given file content.
    """
    for line in content:
        if line == "":
            break
        data, = re.findall(
            r"p=([-]?\d+),([-]?\d+) v=([-]?\d+),([-]?\d+)", line)
        yield robot(*map(int, data))


def main():
    # data = ("example", 11, 7)
    data = ("input", 101, 103)

    content = readfile(data[0])
    robots = [r for r in parse_robots(content)]
    br = bathroom(robots, data[1], data[2])
    time: int = 0
    tree_time = None
    safety_factor = None
    while time <= 100 or tree_time is None:
        if br.is_christmas_tree() and tree_time is None:
            tree_time = time
        if time == 100:
            safety_factor = br.safety_factor()
            print("part 1:", safety_factor)
        br.step()
        time += 1
    print("part 2:", tree_time)


main()
