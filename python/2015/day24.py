import itertools
import math
import sys

from support import InputReader, asserter, timing


def quantum(nums: list[int], groups: int) -> int:
    nums = sorted(nums)
    total = sum(nums)
    target = total // groups

    for i in range(1, len(nums)):
        for comb in itertools.combinations(nums, i):
            if sum(comb) == target:
                return math.prod(comb)

    raise AssertionError("unreachable")


@asserter
def part1(input: list[int]) -> int:
    return quantum(input, 3)


@asserter
def part2(input: list[int]) -> int:
    return quantum(input, 4)


@timing("day24")
def main() -> int:
    i = InputReader(2015, 24).lines

    example = [int(x) for x in i("example")]
    puzzle = [int(x) for x in i("puzzle")]

    def s1() -> None:
        assert part1(example)(99)
        assert part1(puzzle)(11846773891)

    def s2() -> None:
        assert part2(example)(44)
        assert part2(puzzle)(80393059)

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
