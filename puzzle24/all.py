"""
This program solves both parts of the Day 24 puzzle.

Actually, we cannot say that part 2 is solved by this program. On the contrary,
the program tries to match a sequence of full-adders to the input puzzle, and signals
an exception when this is not possible. This has been used to manually produce the list
of swaps which fixes the problem.
"""

from operator import add, and_
from typing import NamedTuple

from aoc import *


class gate(NamedTuple):
    input1: int
    input2: int
    type: str


class input_problem(NamedTuple):
    filename: str
    swaps: int
    fun: Callable[[int, int], int]


class logic_circuit:

    node_name: list[str]
    node_number: dict[str, int]
    first_gate: int
    nodes: int
    gates: list[gate | bool]
    infl: list[list[int]]
    assignment: list[bool]
    outputs: list[int]
    x_wires: list[int]
    y_wires: list[int]
    toporder: list[int]
    target_output: list[bool]
    swaps: list[int]

    def __init__(self, content: list[str], swaps: list[tuple[str, str]]):
        self.first_gate, self.node_name = self._nodes_list(content)
        self.nodes = len(self.node_name)
        self.node_number = {}
        for i, n in enumerate(self.node_name):
            self.node_number[n] = i
        self.gates = self._gates_list(content, self.node_number)

        for g1, g2 in swaps:
            n1 = self.node_number[g1]
            n2 = self.node_number[g2]
            self.gates[n1], self.gates[n2] = self.gates[n2], self.gates[n1]

        self.infl = [[] for _ in range(self.nodes)]
        for i, g in enumerate(self.gates):
            if type(g) != bool:
                i1, i2, _ = g
                self.infl[i1].append(i)
                self.infl[i2].append(i)

        self.outputs = self.bus_wires("z")
        self.x_wires = self.bus_wires("x")
        self.y_wires = self.bus_wires("y")

        self.toporder = []
        for n in self.outputs:
            self.update_toporder(n, self.toporder, set())
        self.assignment = self.compute_assignment()
        self.swaps = []

    @staticmethod
    def _nodes_list(content: list[str]) -> tuple[int, list[str]]:
        l1: list[str] = []
        i = 0
        while i < len(content):
            line = content[i]
            if line == "":
                break
            g, _ = line.split(": ")
            l1.append(g)
            i += 1
        i += 1
        s: set[str] = set()
        while i < len(content):
            i1, _, i2, _, o = content[i].split()
            s.add(i1)
            s.add(i2)
            s.add(o)
            i += 1
        l2 = list(s.difference(l1))
        l2.sort()
        return len(l1), l1 + l2

    @staticmethod
    def _gates_list(content: list[str], node_number: dict[str, int]) -> list[gate | bool]:
        gates: list[gate | bool] = [False] * len(node_number)
        i = 0
        while i < len(content):
            line = content[i]
            if line == "":
                break
            g, v = line.split(": ")
            n = node_number[g]
            gates[n] = bool(int(v))
            i += 1
        i += 1
        while i < len(content):
            g1, port_type, g2, _, o = content[i].split()
            n1 = node_number[g1]
            n2 = node_number[g2]
            no = node_number[o]
            gates[no] = gate(n1, n2, port_type)
            i += 1
        return gates

    def bus_wires(self, letter: str) -> list[int]:
        i = 0
        result: list[int] = []
        while True:
            z = f"{letter}{i:02}"
            if z in self.node_number:
                result.append(self.node_number[z])
            else:
                break
            i += 1
        return result

    def bus_value(self, letter: str) -> int:
        wires = self.bus_wires(letter)
        v = 0
        for i, n in enumerate(wires):
            if self.assignment[n]:
                v += 1 << i
            i += 1
        return v

    def bus_string(self, letter: str) -> str:
        wires = self.bus_wires(letter)
        s = ""
        for n in wires:
            s = ("1" if self.assignment[n] else "0") + s
        return s

    def update_toporder(self, n: int, toporder: list[int], path: set[int]):
        v = self.gates[n]
        if n in toporder:
            pass
        elif type(v) == bool:
            toporder.append(n)
        else:
            i1, i2, _ = v
            if i1 in path or i2 in path:
                return False
            if not self.update_toporder(i1, toporder, path | {n}):
                return False
            if not self.update_toporder(i2, toporder, path | {n}):
                return False
            toporder.append(n)
        return True

    def compute_assignment(self) -> list[bool]:
        value = [False] * self.nodes
        for n in self.toporder:
            v = self.gates[n]
            if type(v) == bool:
                value[n] = v
            else:
                i1, i2, t = v
                v1 = value[i1]
                v2 = value[i2]
                o = v1 and v2 if t == "AND" else v1 or v2 if t == "OR" else v1 != v2
                value[n] = o
        return value

    def __str__(self) -> str:
        s = ""
        for i in self.toporder:
            v = self.gates[i]
            if type(v) == bool:
                continue
            i1, i2, t = v
            # if self.node_name[i1][0] in "xyz" else "s"+str(i1)
            n1 = self.node_name[i1]
            # if self.node_name[i2][0] in "xyz" else "s"+str(i2)
            n2 = self.node_name[i2]
            # if self.node_name[i][0] in "xyz" else "s"+str(i)
            o = self.node_name[i]
            # if self.node_name[i][0] in "xyz" else "s"+str(i)
            o = self.node_name[i]
            s += f"{n1} {t} {n2} -> {o}\n"
        return s

    def find_gate(self, i1: int, i2: int, t: str) -> int:
        for i, g in enumerate(self.gates):
            if type(g) == bool:
                pass
            if g == gate(i1, i2, t) or g == gate(i2, i1, t):
                return i
        return -1

    def full_adder_match(self, carry: int, i: int) -> int:
        if i >= len(self.x_wires):
            return carry
        s1 = self.find_gate(self.x_wires[i], self.y_wires[i], "XOR")
        if s1 < 0 or s1 in self.outputs:
            raise ValueError(f"i={i} s1: {self.node_name[s1]}")
        s2 = self.find_gate(s1, carry, "XOR")
        if s2 != self.outputs[i]:
            raise ValueError(f"i={i} s2: {self.node_name[s2]} carry: {
                             self.node_name[carry]}")
        c1 = self.find_gate(s1, carry, "AND")
        if c1 < 0 or c1 in self.outputs:
            raise ValueError(f"i={i} c1: {self.node_name[c1]}")
        c2 = self.find_gate(self.x_wires[i], self.y_wires[i], "AND")
        if c2 < 0 or c2 in self.outputs:
            raise ValueError(f"i={i} c2: {self.node_name[c2]}")
        c3 = self.find_gate(c1, c2, "OR")
        if c3 < 0 or (i < len(self.x_wires)-1 and c3 in self.outputs):
            raise ValueError(f"i={i} c3: {self.node_name[c3]}")
        return self.full_adder_match(c3, i+1)

    def adder_match(self):
        _ = self.find_gate(self.x_wires[0], self.y_wires[0], "XOR")
        c00 = self.find_gate(self.x_wires[0], self.y_wires[0], "AND")
        carry = self.full_adder_match(c00, 1)
        if carry != self.outputs[-1]:
            raise ValueError(f"i=-1 carry: {self.node_name[carry]}")


def main():
    content = readfile(data[0])
    c = logic_circuit(content, [])
    print("part 1:", c.bus_value("z"))

    # print(f"  x: {c.bus_value("x"):15} {c.bus_string("x"):>50}")
    # print(f"  y: {c.bus_value("y"):15} {c.bus_string("y"):>50}")
    # print(f"  z: {c.bus_value("z"):15} {c.bus_string("z"):>50}")

    # target_val = data[2](c.bus_value("x"), c.bus_value("y"))
    # target_bin = [ch == "1" for ch in reversed(
    #     f"{target_val:0{len(c.outputs)}b}")]
    # target_str = "".join(["1" if v else "0" for v in reversed(target_bin)])

    # print(f"tgt: {target_val:15} {target_str:>50}")

    swaps = [("vvr", "z08"), ("bkr", "rnq"), ("tfb", "z28"), ("mqh", "z39")]

    c = logic_circuit(content, swaps)
    c.adder_match()
    flat_swaps = [x for pair in swaps for x in pair]

    print("part 2:", ",".join(sorted(flat_swaps)))


data = input_problem("input", 4, add)
# data = input_problem("example2", 2, and_)


main()
