"""
This program solves part 2 of Day 1 puzzle.
"""

from collections import defaultdict

l: list[int] = []
d: dict[int, int] = defaultdict(int)
with open("puzzle1/input") as file:
    for line in file:
        v1, v2 = (int(v.strip()) for v in line.strip().split())
        l.append(v1)
        d[v2] += 1

similarity = sum(x*d[x] for x in l)
print(similarity)
