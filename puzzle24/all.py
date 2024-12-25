"""
This program solves both parts of the Day 24 puzzle.

Actually, we cannot say that part 2 is solved by this program. On the contrary,
the program tries to match a chain of full-adders to the puzzle input, and signals
an exception when this is not possible. This has been used to manually produce the list
of swaps which fixes the problem.
"""

from typing import NamedTuple

from aoc import *


class gate(NamedTuple):
    """
    A gate has two input and a type (AND, OR, XOR).
    """
    input1: str
    input2: str
    type: str


class logic_circuit:
    """
    Represent a logic circuit.
    """

    gates: dict[str, gate | bool]
    """Map from wirename to gate or bool (for input wires)."""

    assignment: dict[str, bool]
    """Assignment of booleans to wires."""

    z_wires: list[str]
    """Wires for the z bus."""

    x_wires: list[str]
    """Wires for the x bus."""

    y_wires: list[str]
    """Wires for the y bus."""

    toporder: list[str]
    """Topological order for wires."""

    def __init__(self, content: list[str], swaps: list[tuple[str, str]]):
        """
        Initialize the circuit with the content of a file and a list of wires
        to be swapped.
        """
        self._gates_list(content)

        for g1, g2 in swaps:
            self.gates[g1], self.gates[g2] = self.gates[g2], self.gates[g1]

        self.z_wires = self.bus_wires("z")
        self.x_wires = self.bus_wires("x")
        self.y_wires = self.bus_wires("y")

        self._compute_toporder()
        self._compute_assignment()


    def _gates_list(self, content: list[str]):
        """
        Initialize the gates dictionary with the file content.
        """
        self.gates = {}
        i = 0
        while i < len(content):
            line = content[i]
            if line == "":
                break
            g, v = line.split(": ")
            self.gates[g] = bool(int(v))
            i += 1
        i += 1
        while i < len(content):
            g1, port_type, g2, _, o = content[i].split()
            self.gates[o] = gate(g1, g2, port_type)
            i += 1


    def bus_wires(self, letter: str) -> list[str]:
        """
        Return (in order) list of wires beginning with `letter`.
        """
        i = 0
        result: list[str] = []
        while True:
            z = f"{letter}{i:02}"
            if z in self.gates:
                result.append(z)
            else:
                break
            i += 1
        return result

    def bus_value(self, letter: str) -> int:
        """
        Return the numerical value represented by the wires beginning with `letter`.
        """
        wires = self.bus_wires(letter)
        v = 0
        for i, n in enumerate(wires):
            if self.assignment[n]:
                v += 1 << i
            i += 1
        return v

    def _compute_toporder(self):
        """
        Initializete topological order of wires (assuming there are no loops).
        """
        self.toporder = []

        def update_toporder(g: str):
            v = self.gates[g]
            if g in self.toporder:
                pass
            elif type(v) == bool:
                self.toporder.append(g)
            else:
                i1, i2, _ = v
                update_toporder(i1)
                update_toporder(i2)
                self.toporder.append(g)
            return True

        for g in self.z_wires:
            update_toporder(g)

    def _compute_assignment(self):
        """
        Propagate the signal and initialize the assignment.

        It require the topological order to be computed in advance.
        """
        self.assignment = {}
        for n in self.toporder:
            v = self.gates[n]
            if type(v) == bool:
                self.assignment[n] = v
            else:
                i1, i2, t = v
                v1 = self.assignment[i1]
                v2 = self.assignment[i2]
                o = v1 and v2 if t == "AND" else v1 or v2 if t == "OR" else v1 != v2
                self.assignment[n] = o

    def __str__(self) -> str:
        """
        String representation of the gates in topological order.
        """
        s = ""
        for i in self.toporder:
            v = self.gates[i]
            if type(v) == bool:
                continue
            i1, i2, t = v
            s += f"{i1} {t} {i2} -> {i}\n"
        return s

    def find_gate(self, i1: str, i2: str, t: str) -> str:
        """
        Find a gate with given inputs and type.

        Return the empty string if the gate does not exist.
        """
        for n, g in self.gates.items():
            if type(g) == bool:
                pass
            if g == gate(i1, i2, t) or g == gate(i2, i1, t):
                return n
        return ""

    def full_adder_match(self, carry: str, i: int) -> str:
        """
        Try to match a chain of `i` full adders. The wire `carry` come from
        the outside.
        """
        if i >= len(self.x_wires):
            return carry
        s1 = self.find_gate(self.x_wires[i], self.y_wires[i], "XOR")
        if s1 == "" or s1 in self.z_wires:
            raise ValueError(f"i={i} s1: {s1}")
        s2 = self.find_gate(s1, carry, "XOR")
        if s2 != self.z_wires[i]:
            raise ValueError(f"i={i} s2: {s2}")
        c1 = self.find_gate(s1, carry, "AND")
        if c1 == "" or c1 in self.z_wires:
            raise ValueError(f"i={i} c1: {c1}")
        c2 = self.find_gate(self.x_wires[i], self.y_wires[i], "AND")
        if c2 == "" or c2 in self.z_wires:
            raise ValueError(f"i={i} c2: {c2}")
        c3 = self.find_gate(c1, c2, "OR")
        if c3 == "" or (i < len(self.x_wires)-1 and c3 in self.z_wires):
            raise ValueError(f"i={i} c3: {c3}")
        return self.full_adder_match(c3, i+1)

    def adder_match(self):
        """
        Try to match the circuit to a complete adder which sums x and y bus to
        get the z bus.
        """
        _ = self.find_gate(self.x_wires[0], self.y_wires[0], "XOR")
        c00 = self.find_gate(self.x_wires[0], self.y_wires[0], "AND")
        carry = self.full_adder_match(c00, 1)
        if carry != self.z_wires[-1]:
            raise ValueError(f"i=last carry: {carry}")


def main():
    content = readfile("input")
    c = logic_circuit(content, [])
    print("part 1:", c.bus_value("z"))

    swaps = [("vvr", "z08"), ("bkr", "rnq"), ("tfb", "z28"), ("mqh", "z39")]
    c = logic_circuit(content, swaps)
    c.adder_match()
    flat_swaps = [x for pair in swaps for x in pair]
    print("part 2:", ",".join(sorted(flat_swaps)))


main()
