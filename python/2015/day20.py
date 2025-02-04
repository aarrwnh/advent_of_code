import math
import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


def brute_factors(n: int) -> Generator[int]:
    i = 1
    div = int(math.sqrt(n))
    while i <= div:
        if n % i == 0:
            yield i  # lower member
            yield n // i  # upper member
        i += 1


@asserter
def part1(target: int) -> int:
    n = 0
    while True:
        n += 1
        if sum(set(brute_factors(n))) * 10 > target:
            break
    return n


def filter(n: int, factors: Generator[int]) -> Generator[int]:
    for f in factors:
        if f * 50 >= n:
            yield f


@asserter
def part2(target: int) -> int:
    n = 0
    while True:
        n += 1
        if sum(set(filter(n, brute_factors(n)))) * 11 > target:
            break
    return n


@asserter
def part2_2(target: int, m: int, limit: int) -> int:
    d = target // m
    counts = [0] * d

    for h in range(1, d):
        for e in range(1, min(d // h, limit) + 1):
            counts[e * h - 1] += h * m
        if counts[h - 1] > target:
            return h

    raise AssertionError("unreachable")


@timing("day20")
def main() -> int:
    i = InputReader(2015, 20).raw

    puzzle = int(i("puzzle"))

    def s1() -> None:
        assert part1(150)(10)
        assert part2_2(puzzle, 10, sys.maxsize)(776160)

    def s2() -> None:
        assert part2(150)(8)
        assert part2_2(puzzle, 11, 50)(786240)

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
