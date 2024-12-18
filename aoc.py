"""
A module with utilty classes and functions for AoC.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path
from typing import TextIO

import __main__

type file_content = list[str]


def readfile(filename: str) -> file_content:
    """
    Read an entire file.
    """
    with open(str(Path(__main__.__file__).parent / filename)) as f:
        return f.read().splitlines()


def openfile(filename: str) -> TextIO:
    """
    Open a file in the correct directory.
    """
    return open(str(Path(__main__.__file__).parent / filename))


class multidict[K, V]:
    def __init__(self):
        """
        Initialize the multi dictionary.
        """
        self._dict: dict[K, set[V]] = defaultdict(set)

    def add(self, key: K, value: V):
        """
        Add value V to key K.
        """
        self._dict[key].add(value)

    def check(self, key: K, value: V) -> bool:
        """
        Check if V is associated to K
        """
        return value in self._dict[key]


class priority_queue[V]:
    """
    A priority queue for elements of type V. Its implementation in terms of heaps is
    taken from the online Python reference manual.
    """
    @dataclass(order=True)
    class _Entry:
        """
        An entry containing a value and a priority. The entry is ordered according
        to priority.
        """
        value: V | None = field(compare=False)
        priority: int

    def __init__(self):
        """
        Initialize an empty priority queue.
        """
        self.entry_finder: dict[V, priority_queue._Entry] = {}
        self.heap: list[priority_queue._Entry] = []

    def add(self, value: V, priority: int):
        """
        Add an element to the priority queue or update its priority.
        """
        if value in self.entry_finder:
            entry = self.entry_finder[value]
            entry.value = None
        entry = priority_queue._Entry(value, priority)
        self.entry_finder[value] = entry
        heappush(self.heap, entry)

    def pop(self) -> V | None:
        """
        Extract the element with lowest priority.
        """
        while self.heap:
            entry = heappop(self.heap)
            if entry.value is not None:
                del self.entry_finder[entry.value]
                return entry.value
        return None
