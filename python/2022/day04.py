import re

from support import check_result, read_file, timing  # type: ignore

NON_NUMBER = re.compile(r"[-,]")


def split_pairs(line: str):
    #  [a, b], [c, d] = [
    #      [int(z) for z in y.split("-")] for y in [x for x in line.split(",")]
    #  ]
    return [int(x) for x in NON_NUMBER.split(line)]


@timing()
def part1(pairs: list[str]) -> int:
    total = 0
    for pair in pairs:
        a, b, c, d = split_pairs(pair)
        if a >= c and b <= d or c >= a and d <= b:
            total += 1
    return total


@timing()
def part2(pairs: list[str]):
    total = 0
    for pair in pairs:
        a, b, c, d = split_pairs(pair)
        p2 = range(c, d + 1)
        for i in range(a, b + 1):
            if i in p2:
                total += 1
                break
    return total


def main() -> int:
    sample = read_file(__file__, "../../input/2022/04/sample.input")
    puzzle = read_file(__file__, "../../input/2022/04/puzzle.input")

    check_result(2, part1(sample))
    check_result(569, part1(puzzle))

    check_result(4, part2(sample))
    check_result(936, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
