import math
import sys

from support import InputReader, asserter, timing


OPS = {"*": math.prod, "+": sum}


@asserter
def part1(input: str) -> int:
    lines = input.splitlines()
    ops = lines.pop().split()
    n = [x.split() for x in lines]
    total = 0
    for i, a in enumerate(zip(*n)):
        nums = tuple(int(x) for x in a)
        total += OPS[ops[i]](nums)
    return total


@asserter
def part2(input: str) -> int:
    lines = input.splitlines()
    ops = [(i, n) for i, n in enumerate(lines.pop()) if n != " "]
    n: list[list[str]] = []
    for line in lines:
        s = 0
        out: list[str] = []
        for i in range(1, len(ops)):
            # start = ops[i - 1][0]
            end = ops[i][0]
            out.append(line[s:end])
            s = end
        out.append(line[s:] + " ")
        n.append(out)

    total = 0
    for *a, op in zip(*n, ops):
        nums: list[int] = []
        # slice numbers vertically
        for b in zip(*a):
            v = "".join(b).strip()
            if v != "":
                nums.append(int(v))

        total += OPS[op[1]](nums)

    return total


@timing("day6")
def main() -> int:
    i = InputReader(2025, 6).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(4277556)
        assert part1(puzzle)(5873191732773)

    def s2() -> None:
        assert part2(example)(3263827)
        assert part2(puzzle)(11386445308378)

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
