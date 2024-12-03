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
        l = [int(x) for x in line.split()]
        if is_safe(l): count += 1
print(count)
