import re
import sys

from support import InputReader, asserter, timing


@asserter
@timing("part1")
def part1(input: str) -> int:
    total = 0
    r = re.compile(r"mul\((\d+),(\d+)\)")
    for a in r.finditer(input):
        if a.group(0).startswith("mul"):
            total += int(a.group(1)) * int(a.group(2))
    return total


@asserter
@timing("part2")
def part2(input: str) -> int:
    total = 0
    enable = True
    r = re.compile(r"(do\(\)|don't\(\)|mul\((\d+),(\d+)\))")
    for a in r.finditer(input):
        if a.group(1).startswith("mul"):
            if enable:
                total += int(a.group(2)) * int(a.group(3))
        else:
            enable = not a.group(1).startswith("don't")
    return total


def main() -> int:
    i = InputReader(2024, 3).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(161)
        assert part1(puzzle)(155955228)

    def s2() -> None:
        assert part2(
            "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        )(48)
        assert part2(puzzle)(100189366)

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
