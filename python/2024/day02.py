import sys
from collections.abc import Generator

from support import InputReader, asserter


def is_safe(report: list[int]) -> bool:
    a = [report[i] - report[i + 1] for i in range(len(report) - 1)]
    return (
        # increasing
        a[0] < 0 and all(map(lambda x: -1 >= x >= -3, a))
    ) or (
        # decreasing
        a[0] > 0 and all(map(lambda x: 1 <= x <= 3, a))
    )


def parse(lines: list[str]) -> Generator[list[int], None, None]:
    for line in lines:
        yield [int(v) for v in line.split(" ")]


@asserter
def part1(lines: list[str]) -> int:
    return sum(is_safe(report) for report in parse(lines))


@asserter
def part2(lines: list[str]) -> int:
    safe = 0
    for report in parse(lines):
        for i in range(len(report)):
            if is_safe(report[:i] + report[i + 1 :]):
                safe += 1
                break
    return safe


def main() -> int:
    i = InputReader(2024, 2).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(2)
        assert part1(puzzle)(606)

    def s2() -> None:
        assert part2(example)(4)
        assert part2(puzzle)(644)

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
