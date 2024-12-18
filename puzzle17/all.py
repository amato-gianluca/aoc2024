"""
This program solves both parts of the Day 17 puzzle.
"""

from aoc import *


class cpu:
    """
    CPU simulator.
    """

    def __init__(self, mem: list[int], regs: list[int]):
        """
        Initialize a CPU by connecting its memory and set of registers.
        """
        self.mem = mem
        """Memory connected to the CPU"""
        self.regs = regs
        """Set of registers of the CPU"""
        self.out: list[int] = []
        """Output of the CPU"""
        self.ip: int = 0
        """Instruction pointer register"""
        self.halted: bool = False
        """Halt state"""

    def combo(self, v: int) -> int:
        """
        Evaluates a combo operand.
        """
        if v < 4:
            return v
        elif v < 7:
            return self.regs[v - 4]
        else:
            raise ValueError("Unexpected operand")

    def step(self):
        """
        Execute a single instruction.
        """
        if self.ip >= len(self.mem):
            self.halted = True
            return
        opcode = self.mem[self.ip]
        operand = self.mem[self.ip + 1]
        self.ip += 2
        match opcode:
            case 0:  # adv
                self.regs[0] = self.regs[0] // (2 ** self.combo(operand))
            case 1:  # bxl
                self.regs[1] ^= operand
            case 2:  # bst
                self.regs[1] = self.combo(operand) % 8
            case 3:  # jnz
                if self.regs[0] != 0:
                    self.ip = operand
            case 4:  # bxc
                self.regs[1] ^= self.regs[2]
            case 5:  # out
                self.out.append(self.combo(operand) % 8)
            case 6:  # bdv
                self.regs[1] = self.regs[0] // (2 ** self.combo(operand))
            case 7:  # cdv
                self.regs[2] = self.regs[0] // (2 ** self.combo(operand))
            case _:
                raise ValueError("Unexpected opcode")

    def execute(self):
        """
        Execute the program in memory.
        """
        while not self.halted:
            self.step()


def read_data(filename: str) -> tuple[list[int], list[int]]:
    """
    Read memory and initial register values from a file.
    """
    regs: list[int] = []
    with openfile(filename) as f:
        for _ in range(3):
            regs.append(int(f.readline().split(":")[1]))
        f.readline()
        mem = list(map(int, f.readline().split(":")[1].split(",")))
    return regs, mem


def find_num(mem: list[int], v: int, i: int) -> int | None:
    """
    Assuming that a CPU executing program `mem` with initial value for register
    A equal to `v` produce mem[i+1:] as output, return the initial value for
    register A which produces mem as output.
    """
    if i < 0:
        return v
    else:
        for piece in range(8):
            newv = v * 8 + piece
            pc = cpu(mem, [newv, 0, 0])
            pc.execute()
            if pc.out[0] == mem[i]:
                res = find_num(mem, newv, i-1)
                if res is not None:
                    return res
        return None


def main():
    regs, mem = read_data("input")
    pc = cpu(mem, regs)
    pc.execute()
    print("part 1:", ",".join(map(str, pc.out)))
    print("part 2:", find_num(mem, 0, len(mem)-1))


main()
