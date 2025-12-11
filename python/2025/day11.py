import math
import sys
from functools import cache

from support import InputReader, asserter, timing


@asserter
def part1(input: list[str]) -> int:
    return solve(input, ("you", "out"))


@asserter
def part2(input: list[str]) -> int:
    return solve(
        input,
        ("svr", "dac", "fft", "out"),
        ("svr", "fft", "dac", "out"),
    )


def solve(input: list[str], *paths: tuple[str, ...]) -> int:
    graph: dict[str, list[str]] = {}
    for line in input:
        src, trg0 = line.split(": ")
        graph[src] = trg0.split()

    @cache
    def count(src: str, trg: str) -> int:
        if src == trg:
            return 1
        return sum(count(s, trg) for s in graph.get(src, []))

    return sum(
        math.prod(count(path[i], path[i + 1]) for i in range(len(path) - 1))
        for path in paths
    )


@timing("day11")
def main() -> int:
    i = InputReader(2025, 11).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(5)
        assert part1(puzzle)(652)

    def s2() -> None:
        assert part2(puzzle)(362956369749210)

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
