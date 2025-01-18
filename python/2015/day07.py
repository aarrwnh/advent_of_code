import sys

from support import InputReader, asserter, timing

Wire = str
Signal = tuple[str, ...]

MASK = (1 << 16) - 1


def operation(op: str, left: None | int, right: None | int) -> None | int:
    if left is None or right is None:
        return None

    match op:
        case "AND":
            return left & right
        case "OR":
            return left | right
        case "LSHIFT":
            return left << right
        case "RSHIFT":
            return left >> right
        case "NOT":
            return right ^ MASK
        case _:
            raise AssertionError("unreachable")


def parse(registers: dict[Wire, int], signal: Signal) -> None | int:
    match signal:
        case (value,):
            if value.isdigit():
                return int(value)
            return registers.get(value)

        case (left, op, right):
            right_val = registers.get(right)
            if right_val is not None and left.isdigit():
                return operation(op, int(left), right_val)

            left_val = registers.get(left)
            if left_val is not None and right.isdigit():
                return operation(op, left_val, int(right))

            if left_val is not None and right_val is not None:
                return operation(op, left_val, right_val)

        case (not_, right):
            return operation(not_, 0, registers.get(right))

        case _:
            raise AssertionError("unreachable")
    return None


# class Signal:
#     op: str | None
#     left: str | int | None
#     right: str | int | None
#     value: int | None


def emulate(lines: list[str], read_wire: Wire, overwrites: dict[Wire, int]) -> int:
    instructions: list[tuple[Wire, Signal]] = []
    for line in lines:
        l_s, wire = line.split(" -> ")
        signal = tuple(l_s.split(" "))
        instructions.append((wire, signal))

    for w, v in overwrites.items():
        for i, (s, _) in enumerate(instructions):
            if s == w:
                instructions[i] = (w, tuple([str(v)]))

    registers: dict[Wire, int] = {}

    while instructions:
        newinst = []
        for x in instructions:
            res = parse(registers, x[1])
            if res is not None:
                registers[x[0]] = res
            else:
                newinst.append(x)
        instructions = newinst

    return registers[read_wire]


@asserter
def part1(lines: list[str], read_wire: str) -> int:
    return emulate(lines, read_wire, {})


@asserter
def part2(lines: list[str], overwrite: int) -> int:
    return emulate(lines, "a", {"b": overwrite})


@timing("day7")
def main() -> int:
    i = InputReader(2015, 7).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, "h")(65412)
        assert part1(puzzle, "a")(46065)

    def s2() -> None:
        assert part2(puzzle, 46065)(14134)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
