"""
This program solves both parts of Day 2 puzzle.
"""

def is_safe_with_dampener(l):
    """
    Determines whether report l is safe, using the Problem Dampener.
    """
    if is_safe(l): return True
    for i in range(len(l)):
        l1 = list(l)
        del l1[i]
        if is_safe(l1): return True
    return False

def is_safe(l):
    """
    Determines whether report l is safe, without the use of the Problem Dampener.
    """
    is_increasing = 1 if l[1] - l[0] > 0 else -1
    for i in range(len(l)-1):
        gap = (l[i+1] - l[i]) * is_increasing
        if gap < 1 or gap > 3:
            return False
    return True

with open("puzzle2/input") as file:
    count = 0
    count_dampener = 0
    for line in file:
        l =  [int(x) for x in line.split()]
        count += is_safe(l)
        count_dampener += is_safe_with_dampener(l)

print("part 1:", count)
print("part 2:", count_dampener)
