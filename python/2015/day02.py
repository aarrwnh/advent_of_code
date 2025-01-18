import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


def parse(lines: list[str]) -> Generator[list[int], None, None]:
    for dimensions in lines:
        yield [int(x) for x in dimensions.split("x")]


@asserter
def part1(lines: list[str]) -> int:
    total = 0
    for l, w, h in parse(lines):
        a = [l * w, w * h, h * l]
        total += min(a) + sum(2 * x for x in a)
    return total


@asserter
def part2(lines: list[str]) -> int:
    total = 0
    for l, w, h in parse(lines):
        a = 2 * l + 2 * w
        b = 2 * w + 2 * h
        c = 2 * h + 2 * l
        total += min(a, b, c) + l * w * h
    return total


@timing("day02")
def main() -> int:
    i = InputReader(2015, 2).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(["2x3x4"])(58)
        assert part1(puzzle)(1586300)

    def s2() -> None:
        assert part2(["2x3x4"])(34)
        assert part2(puzzle)(3737498)

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
