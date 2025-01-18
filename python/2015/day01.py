import sys

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    floor = 0
    for ch in input:
        if ch == "(":
            floor += 1
        elif ch == ")":
            floor -= 1
    return floor


@asserter
def part2(input: str) -> int:
    floor = 0
    for i, ch in enumerate(input):
        if ch == "(":
            floor += 1
        elif ch == ")":
            floor -= 1
        if floor == -1:
            return i + 1
    raise AssertionError("unreachable")


@timing("day01")
def main() -> int:
    i = InputReader(2015, 1).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(74)

    def s2() -> None:
        assert part2(puzzle)(1795)

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
