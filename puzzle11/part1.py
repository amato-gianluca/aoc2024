"""
This program solves part 1 of the Day 11 puzzle by simulating the evolution
of the sequence of stones. This does not scale up for part 2.
"""

from aoc import *


def blink_line(line: list[int]) -> list[int]:
    """
    Blink the line and returns the new line.
    """
    new_line: list[int] = []
    for x in line:
        if x == 0:
            new_line.append(1)
        elif (sizex := len(str(x))) % 2 == 0:
            pow = 10 ** (sizex // 2)
            new_line.append(x // pow)
            new_line.append(x % pow)
        else:
            new_line.append(x * 2024)
    return new_line


def parse_line(line: str) -> list[int]:
    """
    Parse the input line.
    """
    return list(map(int, line.split()))


def main():
    content = readfile("input")
    line = parse_line(content[0])

    #print(f"step 0 length {len(line)}")
    #print(line)
    for i in range(25):
        line = blink_line(line)
        #print(f"step {i+1} length {len(line):_}")
        #if len(line) < 100: print(line)
    print("part 1:", len(line))
    # An attemp to run 75 iterations fails at iteration 45 on my PC, since the process is
    # killed by the OOM killer.
    # At iteration 44, the line was 606_737_523 positions long


main()
