import sys

from support import InputReader, asserter, timing


@asserter
def part1(lines: list[str]) -> int:
    dial = 50
    count = 0
    for turn in lines:
        n = int(turn[1:])
        n = -n if turn[0] == "L" else n
        dial += n
        dial %= 100
        if dial == 0:
            count += 1
    return count


@asserter
def part2(lines: list[str]) -> int:
    dial = 50
    count = 0
    for turn in lines:
        n = int(turn[1:])

        count += n // 100
        n %= 100
        n = -n if turn[0] == "L" else n

        prev = dial
        dial += n
        if dial <= 0 < prev or dial >= 100:
            count += 1

        dial %= 100

    return count


@timing("day1")
def main() -> int:
    i = InputReader(2025, 1).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(3)
        assert part1(puzzle)(1071)

    def s2() -> None:
        assert part2(example)(6)
        assert part2(puzzle)(6700)

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
