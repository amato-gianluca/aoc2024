"""
This program solves both parts of the Day 10 puzzle.
"""

type topomap = list[list[int]]
"""A topological map."""

type position = tuple[int, int]
"""A position in map."""


def trails_from(m: topomap, pos: position) -> tuple[set[position], int]:
    """
    Returns the set of 9-height positions reachable from pos, and the number of distinct
    hiking trails to reach them.
    """
    i, j = pos
    val = m[i][j]
    if val == 9:
        return {pos}, 1
    else:
        tails: set[position] = set()
        count = 0
        for new_pos in [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]:
            new_i, new_j = new_pos
            if 0 <= new_i < len(m) and 0 <= new_j < len(m[0]) and  m[new_i][new_j] == val + 1:
                new_tails, new_count = trails_from(m, new_pos)
                tails.update(new_tails)
                count += new_count
        return tails, count


def trail_score(m: topomap) -> tuple[int, int]:
    """
    Returns total sum of tailheads rating and score.
    """
    score = 0
    rating = 0
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == 0:
                tails, count = trails_from(m, (i, j))
                score += len(tails)
                rating += count
    return score, rating


def read_file(filename: str) -> topomap:
    """
    Read a topographic map from the given file.
    """
    m: topomap = []
    with open(filename) as f:
        for line in f:
            m.append([int(ch) for ch in line.rstrip()])
    return m


m = read_file('puzzle10/input')
score, rating = trail_score(m)
print("part 1:", score)
print("part 2:", rating)
