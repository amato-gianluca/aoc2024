"""
This program solves both parts of the Day 8 puzzle.
"""

from collections import defaultdict
from itertools import combinations
from typing import Iterable

type position = tuple[int, int]


class antennas_disposition:
    """
    This class encodes a specific disposition of antennas.

    The attributes are:
    - pos: frequency indexed set of antenna positions
    - num_rows: number of rows in the map
    - num_cols: number of columns in the map
    """

    def __init__(self, filename: str):
        """
        Reads the antennas disposition from the given file.
        """
        self.disposition: dict[str, set[position]] = defaultdict(set)
        self.num_rows = 0
        with open(filename) as f:
            for i, line in enumerate(f):
                line = line.rstrip()
                self.num_rows += 1
                if i == 0:
                    self.num_cols = len(line)
                for j, ch in enumerate(line):
                    if ch.isalnum():
                        self.disposition[ch].add((i, j))

    def is_inside(self, i: int, j: int) -> bool:
        """
        Determines whether a given position is inside the map.
        """
        return 0 <= i < self.num_rows and 0 <= j < self.num_cols


class antinodes:
    """
    This class encodes a set of antinodes of a given antenna disposition.
    """

    def __init__(self, ad: antennas_disposition, harmonics: bool = False):
        """
        Computes the antinodes positions from a given antenna disposition. either
        consider resonant harmonics or not.
        """
        self.ad = ad
        self.harmonics = harmonics
        self.antinodes: list[list[bool]] = [
            [False] * ad.num_cols for _ in range(ad.num_rows)
        ]
        for positions in ad.disposition.values():
            self._antinodes_from_list(positions)

    def _antinodes_from_list(self, positions: Iterable[position]):
        """
        Update the set of antinodes from a given list of antennas. All antennas
        are of the same frequency.
        """
        for ((i0, j0), (i1, j1)) in combinations(positions, 2):
            di = i1 - i0
            dj = j1 - j0
            if self.harmonics:
                i = i1
                j = j1
                while self.ad.is_inside(i, j):
                    self.antinodes[i][j] = True
                    i += di
                    j += dj
                i = i0
                j = j0
                while self.ad.is_inside(i, j):
                    self.antinodes[i][j] = True
                    i -= di
                    j -= dj
            else:
                i = i1 + di
                j = j1 + dj
                if self.ad.is_inside(i, j):
                    self.antinodes[i][j] = True
                i = i0 - di
                j = j0 - dj
                if self.ad.is_inside(i, j):
                    self.antinodes[i][j] = True

    def size(self):
        """
        Returns the number of antinodes.
        """
        return sum(sum(row) for row in self.antinodes)

    # This is just for debugging, not used for the answer
    def __str__(self):
        """
        Returns a map with antinodes positions.
        """
        out = "\n".join(
            "".join(["#" if col else "." for col in row])
            for row in self.antinodes
        )
        return out


ad = antennas_disposition('puzzle8/input')
an1 = antinodes(ad)
an2 = antinodes(ad, True)
print("part 1:", an1.size())
print("part 2:", an2.size())
