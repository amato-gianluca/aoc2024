"""
This program solves both parts of the Day 9 puzzle.
"""

from typing import NamedTuple

from aoc import *


class Block(NamedTuple):
    """
    A named tuple corresponding to a pair (file_id, size).
    """
    file_id: int
    size: int

    def is_free_space(self):
        """
        Return whether the block corresponds to free space
        """
        return self.file_id == -1

    def to_free(self):
        """
        Return a new block of free space of the similar size ot this block.
        """
        return self._replace(file_id=-1)


type compressed_map = list[Block]
"""
A compressed map is a list of blocks, each corresponding to a contiugous space in the
disk assigned to either a file or a free space.
"""

type uncompressed_map = list[int]
"""
An uncompressed map is a sequence of file identifiers (or -1) for free space, each for
a disk sector.
"""


def read_compressed_map(line: str) -> compressed_map:
    """
    Read the specified file and return a file map in the compressed format"
    """
    blocks: compressed_map = []
    id = 0
    free_space = False
    for ch in line:
        if free_space:
            blocks.append(Block(-1, int(ch)))
        else:
            blocks.append(Block(id, int(ch)))
            id += 1
        free_space = not free_space
    return blocks


def defragment_map_block(blocks: compressed_map):
    """
    Defragment a map in compressed format, moving an entire file at a time.
    """
    src = len(blocks)-1
    while src > 0:
        while blocks[src].is_free_space():
            src -= 1
        dst = 0
        for dst in range(src):
            if blocks[dst].is_free_space() and blocks[dst].size >= blocks[src].size:
                gap_size = blocks[dst].size - blocks[src].size
                blocks[dst] = blocks[src]
                blocks[src] = blocks[src].to_free()
                if gap_size:
                    blocks.insert(dst + 1, Block(-1, gap_size))
                    src += 1
                break
        src -= 1


def uncompress_map(blocks: compressed_map) -> uncompressed_map:
    """
    Convert a compressed file map into an uncompressed one.
    """
    um: list[int] = []
    for id, size in blocks:
        um += [id] * size
    return um


def defragment_map(um: uncompressed_map):
    """
    Defragment a map one sector at a time.
    """
    dst = 0
    src = len(um)-1
    while True:
        while um[dst] != -1:
            dst += 1
        while um[src] == -1:
            src -= 1
        if src <= dst:
            break
        um[dst] = um[src]
        um[src] = -1
        dst += 1
        src -= 1


def compute_checksum(um: uncompressed_map) -> int:
    """
    Compute the checksum of an uncompressed file map.
    """
    return sum(i * v for i, v in enumerate(um) if v != -1)


def main():
    content = readfile("input")
    cm = read_compressed_map(content[0])

    um = uncompress_map(cm)
    defragment_map(um)
    print("part 1:", compute_checksum(um))

    defragment_map_block(cm)
    print("part 2:", compute_checksum(uncompress_map(cm)))


main()
