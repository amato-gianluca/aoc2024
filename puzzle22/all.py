"""
This program solves both parts of the Day 22 puzzle.
"""

from collections import Counter
from functools import reduce

from aoc import *

type prize_changes = tuple[int, int, int, int]

STEPS = 2000
"""Number of steps of the negotiation."""


def parse_input(content: list[str]) -> list[int]:
    """
    Parse the input and return a list of secret numbers.
    """
    return [int(line) for line in content]


def step(secret: int) -> int:
    """
    Perform a single step of pseudo-random number generation.
    """
    secret = (secret ^ (secret << 6)) % 16777216
    secret = (secret ^ (secret >> 5)) % 16777216
    secret = (secret ^ (secret << 11)) % 16777216
    return secret


def simulate(secret: int, n: int) -> int:
    """
    Perform `n` steps of pseudo-random number generations.
    """
    return reduce(lambda x, y: step(x), range(n), secret)


def compute_gains(secret: int, n: int) -> Counter[prize_changes]:
    """
    For a given secret and number of steps, return a dictionary mapping the
    price changes to the attainable gain.
    """
    gains: Counter[prize_changes] = Counter()
    secret_old = secret
    changes: prize_changes = 0, 0, 0, 0
    for i in range(n):
        secret_new = step(secret_old)
        change = (secret_new % 10) - (secret_old % 10)
        changes = (changes[1], changes[2], changes[3], change)
        if i >= 3 and changes not in gains:
            gains[changes] = secret_new % 10
        secret_old = secret_new
    return gains


def merge_gains(buyer_gains: list[Counter[prize_changes]]) -> Counter[prize_changes]:
    """
    Put together the wins of different buyers.
    """
    counter: Counter[prize_changes] = Counter()
    for gain in buyer_gains:
        counter += Counter(gain)
    return counter


def main():
    content = readfile("input")
    secrets = parse_input(content)
    print("part 1:", sum(simulate(secret, STEPS) for secret in secrets))
    buyer_gains = [compute_gains(secret, STEPS) for secret in secrets]
    total_gains = merge_gains(buyer_gains)
    print("part 2:", max(total_gains.values()))


main()
