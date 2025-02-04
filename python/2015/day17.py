import itertools
import sys

from support import InputReader, asserter, timing


def fillable(containers: list[int], rem_amount: int) -> int:
    if rem_amount == 0:
        return 1
    if len(containers) == 0:
        return 0

    n = fillable(containers[1:], rem_amount)

    if rem_amount >= containers[0]:
        n += fillable(containers[1:], rem_amount - containers[0])

    return n


@asserter
def part1(lines: list[str], amount: int = 25) -> int:
    containers = [int(x) for x in lines]

    # for i in range(1, len(containers) + 1):
    #     for comb in itertools.combinations(containers, r=i):
    #         if sum(comb) == amount:

    return fillable(containers, amount)


@asserter
def part2(lines: list[str], amount: int = 25) -> int:
    containers = [int(x) for x in lines]
    for i in range(1, len(containers) + 1):
        count = list(
            x for x in itertools.combinations(containers, r=i) if sum(x) == amount
        )
        if count:
            return len(count)
    return 0


@timing("day17")
def main() -> int:
    i = InputReader(2015, 17).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(4)
        assert part1(puzzle, 150)(1638)

    def s2() -> None:
        assert part2(example)(3)
        assert part2(puzzle, 150)(17)

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
