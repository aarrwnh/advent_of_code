import sys

from support import InputReader, asserter, timing


def find_largest(bank: str, total_batteries: int) -> int:
    nums = tuple(int(n) for n in bank)
    size = len(nums)
    start = 0
    res = 0
    for i in range(1, total_batteries + 1):
        nums0 = nums[start:size - (total_batteries - i)]
        n = max(nums0)
        j = nums0.index(n)
        start += j + 1
        res = res * 10 + n
    return res


@asserter
def part1(lines: list[str]) -> int:
    return sum(find_largest(line, 2) for line in lines)


@asserter
def part2(lines: list[str]) -> int:
    return sum(find_largest(line, 12) for line in lines)


@timing("day3")
def main() -> int:
    i = InputReader(2025, 3).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(357)
        assert part1(puzzle)(17263)

    def s2() -> None:
        assert part2(example)(3121910778619)
        assert part2(puzzle)(170731717900423)

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
