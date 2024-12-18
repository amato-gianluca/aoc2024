"""
This program solves both parts of the Day 4 puzzle.
"""

from aoc import *


def check_word(m: list[str], i: int, j: int, stepi: int, stepj: int, word: str) -> bool:
    """
    Return true if in the character matrix `m`, starting from position (`i`, `j`), and
    using steps (`stepi`, `stepj`), contains `word`. It also works if `m` is jagged.
    """
    for c in word:
        if 0 <= i < len(m) and 0 <= j < len(m[i]) and m[i][j] == c:
            i += stepi
            j += stepj
        else:
            return False
    return True


def search_word(m: list[str], word: str):
    """
    Count the number of times `word` occurs in `m`. It requires `word` NOT TO
    be palindrome.
    """
    count = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] != word[0]:
                continue   # optimization, not really needed
            for stepi in -1, 0, 1:
                for stepj in -1, 0, 1:
                    if stepi == 0 == stepj:
                        continue
                    count += check_word(m, i, j,  stepi, stepj, word)
    return count


def search_x_word(m: list[str], word: str):
    """
    Count the number of times `word` occurs in `m` in X shape.
    """
    count = 0
    for i in range(len(m)):
        lasti = i + len(word) - 1
        for j in range(len(m[i])):
            lastj = j + len(word) - 1
            if check_word(m, i, j, 1, 1, word) or check_word(m, lasti, lastj, -1, -1, word):
                if check_word(m, i, lastj, 1, -1, word) or check_word(m, lasti, j, -1, 1, word):
                    count += 1
    return count


def main():
    matrix = readfile("input")
    print("part 1:", search_word(matrix, "XMAS"))
    print("part 2:", search_x_word(matrix, "MAS"))


main()
