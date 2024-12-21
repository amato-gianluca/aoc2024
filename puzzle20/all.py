"""
This program solves both parts of the Day 20 puzzle.
"""


from aoc import *


class Day20Maze(Maze):
    """
    Extend the Maze class with the support for cheats.
    """

    def cheats(self, pos: tuple[int, int], steps: int) -> list[Maze.position]:
        """
        Return the list of possible cheats starting from `pos` and of length `steps`
        or less.
        """
        i, j = pos
        return [
            (i_new, j_new)
            for i_new in range(i-steps, i+steps+1)
            for j_new in range(j-steps+abs(i_new - i), j+steps+1-abs(i_new - i))
            if 0 <= i_new < self.nrow and 0 <= j_new < self.ncol
            if self.map[i_new][j_new] != "#"
        ]

    def shortest_path_with_cheat(self, steps: int) -> int | None:
        """
        Return the number of cheats of length `steps` or less which makes you
        gain 100 picoseconds or more.
        """
        pos_end = self.i_end, self.j_end
        dijkstra1 = self.dijkstra()
        dijkstra2 = self.dijkstra(pos_end)
        path = dijkstra1.path_compute(pos_end)
        if path is None:
            return None
        length = dijkstra1.dists[pos_end]
        gains = [0] * length
        for pos in path:
            cheats = self.cheats(pos, steps)
            for cheat_pos in cheats:
                first_piece = dijkstra1.dists[pos]
                second_piece = dijkstra2.dists.get(cheat_pos, None)
                if second_piece is not None:
                    gain = length - first_piece - second_piece - \
                        (abs(cheat_pos[0]-pos[0])+abs(cheat_pos[1]-pos[1]))
                    if gain >= 0:
                        gains[gain] += 1
        return sum(gains[100:])


def main():
    content = readfile("input")
    maze = Day20Maze(content)
    print("part 1:", maze.shortest_path_with_cheat(2))
    print("part 2:", maze.shortest_path_with_cheat(20))


main()
