"""
This program solves both parts of the Day 15 puzzle.
"""

from typing import TextIO


class warehouse:

    def __init__(self, map: list[str], wide: bool = False):
        if wide:
            map = [line
                   .replace("#", "##")
                   .replace("O", "[]")
                   .replace(".", "..")
                   .replace("@", "@.")
                   for line in map]
        self.map = [[ch for ch in line] for line in map]
        self.i, self.j = self._find_robot(self.map)
        self.nrow = len(self.map)
        self.ncol = len(self.map[0])

    @staticmethod
    def _find_robot(map: list[list[str]]) -> tuple[int, int]:
        """
        Return the position of the robot in the given map.
        """
        return [(i, j)
                for i, line in enumerate(map)
                for j, obj in enumerate(line)
                if obj == "@"][0]

    @staticmethod
    def _move_to_displacement(m: str) -> tuple[int, int]:
        """
        Convert the move given as a character into vertical and horizontal displacements.
        """
        match m:
            case "<": return 0, -1
            case ">": return 0, 1
            case "^": return -1, 0
            case "v": return 1, 0
            case _: raise ValueError("Invalid move")

    def score(self) -> int:
        """
        Return the sum of the GPS coordinates of all the obstactles.
        """
        return sum(100*i + j
                   for i, line in enumerate(self.map)
                   for j, obj in enumerate(line)
                   if obj in "O[")

    def move(self, m: str):
        """
        Perform the move `m`.
        """
        di, dj = warehouse._move_to_displacement(m)
        if self._can_move(self.i, self.j, di, dj):
            self._real_move(self.i, self.j, di, dj)
            self.map[self.i][self.j] = "."
            self.i += di
            self.j += dj

    def _can_move2(self, i: int, j: int, di: int, dj: int) -> bool:
        """
        Determine whether it is possible to move the object in position (i,j) by
        the displacement (di, dj). I correctly handle the case that in (i,j) we have
        a wide box.
        """
        i += di
        j += dj
        if self.map[i][j] == "#":
            return False
        elif self.map[i][j] == ".":
            return True
        elif self.map[i][j] == "[" and di != 0:
            return self._can_move(i, j, di, dj) and self._can_move(i, j+1, di, dj)
        elif self.map[i][j] == "]" and di != 0:
            return self._can_move(i, j, di, dj) and self._can_move(i, j-1, di, dj)
        else:
            return self._can_move(i, j, di, dj)

    def _can_move(self, i: int, j: int, di: int, dj: int) -> bool:
        """
        Determine whether it is possible to move the object in position (i,j) by
        the displacement (di, dj). It correctly handles the case that (i,j) contains
        a wide box.
        """
        newi = i + di
        newj = j + dj
        match self.map[i][j]:
            case "#":
                return False
            case ".":
                return True
            case w if w in "[]" and di != 0:
                left_pos = newj if w == "[" else newj - 1
                return self._can_move(newi, left_pos, di, dj) and self._can_move(newi, left_pos+1, di, dj)
            case _:
                return self._can_move(newi, newj, di, dj)

    def _real_move(self, i: int, j: int, di: int, dj: int):
        """
        Move the object in position (i, j) by the displacement (di, dj), correctly handling
        the case when (i,j) contains a wide box. It should be called only after checking
        that the move is valid with _can_move.
        """
        newi = i + di
        newj = j + dj
        match self.map[i][j]:
            case ".":
                pass
            case w if w in "[]" and di != 0:
                left_pos = newj if w == "[" else newj - 1
                self._real_move(newi, left_pos, di, dj)
                self._real_move(newi, left_pos+1, di, dj)
                self.map[newi][left_pos] = "["
                self.map[newi][left_pos+1] = "]"
                self.map[i][left_pos] = self.map[i][left_pos+1] = "."
            case _:
                self._real_move(newi, newj, di, dj)
                self.map[newi][newj] = self.map[i][j]
                self.map[i][j] = "."

    def __str__(self):
        return "\n".join("".join(line) for line in self.map)


def read_map(f: TextIO) -> list[str]:
    """
    Read the map from file `f` as a list of strings.
    """
    m: list[str] = []
    while (line := f.readline().strip()) != "":
        m.append(line)
    return m


def read_moves(f: TextIO) -> str:
    """
    Read the moves from file `f` as a single string.
    """
    return "".join(f.read().splitlines())


with open("puzzle15/input") as f:
    w_map = read_map(f)
    moves = read_moves(f)

w1 = warehouse(w_map)
for m in moves:
    w1.move(m)
print("part 1:", w1.score())

w2 = warehouse(w_map, wide=True)
for m in moves:
    w2.move(m)
print("part 2:", w2.score())
