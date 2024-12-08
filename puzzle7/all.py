"""
This program solves both parts of the Day 7 puzzle.
"""


def feasible(operands: list[int], pos: int, result: int, allow_concatenation: bool = False) -> bool:
    """
    Returns true if it is possible to select operators for the sublist `operands[:pos+1]` in such
    a way that we get the value `result`. The `allow_concatenation` flag determines whether the
    concatenation operator is allowed or not.
    """
    if pos == 0:
        return result == operands[0]
    # Try sum
    if (newval := result - operands[pos]) > 0 and feasible(operands, pos-1, newval, allow_concatenation):
        return True
    # Try product
    if result % operands[pos] == 0 and feasible(operands, pos-1, result // operands[pos], allow_concatenation):
        return True
    # Try concatenation
    if allow_concatenation:
        magnitude = 10 ** len(str(operands[pos]))
        if (newval := result - operands[pos]) % magnitude == 0 and feasible(operands, pos-1, newval // magnitude, allow_concatenation):
            return True
    return False


def parse_line(line: str) -> tuple[list[int], int]:
    """
    Parse a single line of the file in a pair made of a sequence of operand and the sought result.
    """
    l1, l2 = line.split(":")
    return list(map(int, l2.split())), int(l1)


part1 = part2 = 0
with open("puzzle7/input") as file:
    for line in file:
        operands, result = parse_line(line)
        if feasible(operands, len(operands) - 1, result):
            part1 += result
            part2 += result
        elif feasible(operands, len(operands) - 1, result, allow_concatenation=True):
            part2 += result

print("part 1:", part1)
print("part 2:", part2)
