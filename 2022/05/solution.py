import math
import re
from typing import NamedTuple

from support import check_result, read_file_all, timing  # type: ignore


class Instruction(NamedTuple):
    amount: int
    move_from: int
    move_to: int

    @classmethod
    def parse(cls, instr: str):
        a = [int(x.group()) for x in re.finditer(r"(\d+)", instr)]
        return cls(amount=a[0], move_from=a[1] - 1, move_to=a[2] - 1)


def transform_stack(stack: str) -> dict[int, list[str]]:
    init_lines = stack.split("\n")
    range_stop = math.ceil(len(init_lines[0]) / 4)
    stacks: dict[int, list[str]] = {x: [] for x in range(0, range_stop)}
    #  print(len(init_lines[0]))
    for idx in range(0, len(init_lines) - 1):
        line = init_lines[idx]
        for x in range(0, range_stop):
            crate = line[x * 4 : x * 4 + 3].strip()
            if crate != "":
                stacks[x].insert(0, crate[1])
    return stacks


@timing()
def part1(input: str) -> str:
    init, instructions = input.split("\n\n")
    stacks = transform_stack(init)

    for instr in instructions.strip().split("\n"):
        i = Instruction.parse(instr)
        stack = stacks[i.move_from]
        for _ in range(i.amount):
            stacks[i.move_to].append(stack.pop())

    return "".join([x.pop() for x in stacks.values()])


@timing()
def part2(input: str) -> str:
    init, instructions = input.split("\n\n")
    stacks = transform_stack(init)

    for instr in instructions.strip().split("\n"):
        i = Instruction.parse(instr)
        stack = stacks[i.move_from]

        for x in stack[len(stack) - i.amount : len(stack)]:
            stacks[i.move_to].append(x)

        for _ in range(i.amount):
            stack.pop()

    return "".join([x.pop() for x in stacks.values()])


def main() -> int:
    sample = read_file_all(__file__, "../../input/2022/05/sample.input")
    puzzle = read_file_all(__file__, "../../input/2022/05/puzzle.input")

    check_result("CMZ", part1(sample))
    check_result("HNSNMTLHQ", part1(puzzle))

    check_result("MCD", part2(sample))
    check_result("RNLFDJMCT", part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
