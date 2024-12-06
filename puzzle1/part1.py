"""
This program solves part 1 of Day 1 puzzle.
"""

l1: list[int] = []
l2: list[int] = []
with open("puzzle1/input") as file:
    for line in file:
        v1, v2 = (int(v.strip()) for v in line.strip().split())
        l1.append(v1)
        l2.append(v2)
l1.sort()
l2.sort()
totdiff = sum(abs(a-b) for a, b in zip(l1, l2))
print(totdiff)
