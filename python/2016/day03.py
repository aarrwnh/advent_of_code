import sys
from collections.abc import Iterator

from support import InputReader, asserter, timing


def valid(a: int, b: int, c: int) -> int:
    return a + b > c and a + c > b and b + c > a


def split(line: str) -> Iterator[int]:
    return map(int, line.strip().split())


@asserter
def part1(lines: list[str]) -> int:
    count = 0
    for line in lines:
        count += valid(*split(line))
    return count


@asserter
def part2(lines: list[str]) -> int:
    count = 0
    for column in zip(*(split(line) for line in lines)):
        for i in range(0, len(column), 3):
            count += valid(*column[i:i+3])
    return count


@timing("day03")
def main() -> int:
    i = InputReader(2016, 3).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(1032)

    def s2() -> None:
        assert part2(puzzle)(1838)

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
