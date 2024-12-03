def is_safe_with_dampener(l):
    if is_safe(l): return True
    for i in range(len(l)):
        l1 = list(l)
        del l1[i]
        if is_safe(l1): return True
    return False

def is_safe(l):
    is_increasing = 1 if l[1] - l[0] > 0 else -1
    for i in range(len(l)-1):
        gap = (l[i+1] - l[i]) * is_increasing
        if gap < 1 or gap > 3:
            return False
    return True

with open("puzzle2/input") as file:
    count = 0
    for line in file:
        l =  [int(x) for x in line.split()]
        if is_safe_with_dampener(l): count += 1
print(count)
