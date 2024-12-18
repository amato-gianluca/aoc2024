"""
This program solves both parts of the Day 3 puzzle.
"""

from aoc import *


class Computer:
    """
    A computer that understands instructions mul, do and don't.
    """

    def __init__(self):
        """
        Initialize the computer.
        """
        self._total: int = 0
        self._guarded_total: int = 0
        self._guarded: bool = True

    @property
    def total(self) -> int:
        """
        Return the total of all mul instructions, independently from the fact
        that the computer was in a guarded state or not.
        """
        return self._total

    @property
    def guarded_total(self) -> int:
        """
        Return the total of all mul instructions executed when the computer
        was in a guarded state.
        """
        return self._guarded_total

    def do(self):
        """
        Go to guarded state.
        """
        self._guarded = True

    def dont(self):
        """
        Exit from guarded state.
        """
        self._guarded = False

    def mul(self, a: int, b: int):
        """
        Multiply `a` and `b`, and update totals.
        """
        mul = a * b
        self._total += mul
        if self._guarded:
            self._guarded_total += mul

    def parse(self, s: str):
        """
        Parse the corrupted program `s` and computes the embedded instructions.
        """
        import re
        it = re.finditer(r"mul\(([0-9]+),([0-9]+)\)|do\(\)|don't\(\)", s)
        for m in it:
            if m[0] == "do()":
                self.do()
            elif m[0] == "don't()":
                self.dont()
            else:
                self.mul(int(m[1]), int(m[2]))


def main():
    computer = Computer()
    content = readfile("input")
    for line in content:
        computer.parse(line)
    print("part 1:", computer.total)
    print("part 2:", computer.guarded_total)


main()
