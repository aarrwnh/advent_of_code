import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


@asserter
def part1(input: list[str]) -> int:
    return roll(input, True)


@asserter
def part2(input: list[str]) -> int:
    return roll(input)


def roll(input: list[str], once: bool = False) -> int:
    grid: set[tuple[int, int]] = set()
    for row, line in enumerate(input):
        for col, ch in enumerate(line):
            if ch == "@":
                grid.add((row, col))

    total = 0
    prev = -1
    while prev != 0:
        new_grid: set[tuple[int, int]] = set()
        can_remove = 0
        for r, c in grid:
            count = 0
            for n in neighbours(r, c):
                count += n in grid
                if count >= 4:
                    break
            if count < 4:
                can_remove += 1
            else:
                new_grid.add((r, c))

        total += can_remove
        if once:
            break
        prev = can_remove
        grid = new_grid

    return total


def neighbours(r: int, c: int) -> Generator[tuple[int, int]]:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == dc == 0:
                continue
            yield dr + r, dc + c


@timing("day4")
def main() -> int:
    i = InputReader(2025, 4).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(13)
        assert part1(puzzle)(1344)

    def s2() -> None:
        assert part2(example)(43)
        assert part2(puzzle)(8112)

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
