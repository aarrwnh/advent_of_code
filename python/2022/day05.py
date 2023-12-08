import math
import re
from typing import NamedTuple

from support import assert_result, read_file_raw, timing  # type: ignore


class Instruction(NamedTuple):
    amount: int
    move_from: int
    move_to: int

    @classmethod
    def parse(cls, instr: str):
        a = [int(x.group()) for x in re.finditer(r"(\d+)", instr)]
        return cls(a[0], a[1] - 1, a[2] - 1)


def parse_input(input: str) -> tuple[list[str], dict[int, list[str]]]:
    stack, instructions = input.split("\n\n")
    range_stop = math.ceil(input.index("\n") / 4)
    lines = stack.split("\n")
    stacks: dict[int, list[str]] = {x: [] for x in range(0, range_stop)}

    for x in range(0, len(lines) - 1):  # skip the last line with numbers
        for i, crate in enumerate(lines[x][1::4]):
            if not crate.isspace():
                stacks[i].insert(0, crate)

    return instructions.strip().split("\n"), stacks


@timing()
def part1(input: str) -> str:
    instructions, stacks = parse_input(input)

    for instr in instructions:
        i = Instruction.parse(instr)
        stack = stacks[i.move_from]

        for _ in range(i.amount):
            stacks[i.move_to].append(stack.pop())

    return "".join([x.pop() for x in stacks.values()])


@timing()
def part2(input: str) -> str:
    instructions, stacks = parse_input(input)

    for instr in instructions:
        i = Instruction.parse(instr)
        stack = stacks[i.move_from]

        for idx in range(len(stack) - i.amount, len(stack)):
            stacks[i.move_to].append(stack[idx])

        for _ in range(i.amount):
            stack.pop()

    return "".join([x.pop() for x in stacks.values()])


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/05/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/05/puzzle.input")

    assert_result("CMZ", part1(sample))
    assert_result("HNSNMTLHQ", part1(puzzle))

    assert_result("MCD", part2(sample))
    assert_result("RNLFDJMCT", part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
