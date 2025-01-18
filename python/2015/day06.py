import re
import sys
from collections.abc import Generator

from support import InputReader, asserter, timing

P = tuple[int, int]
Grid = list[list[int]]


def new_grid() -> Grid:
    return [[0] * 1000 for _ in range(1000)]


RE_LINE = re.compile(r"(turn on|toggle|turn off) (\d+,\d+) through (\d+,\d+)")


def parse(lines: list[str]) -> Generator[tuple[int, int, int], None, None]:
    for line in lines:
        parts: list[str] = [x for x in RE_LINE.findall(line)[0]]

        inst_s = parts.pop(0)
        inst: int = 0
        if inst_s == "turn on":
            inst = 1
        elif inst_s == "turn off":
            inst = 2

        coords: list[int] = []
        for s in parts:
            coords.extend(int(x) for x in s.split(","))

        ax, ay, bx, by = coords

        for x in range(ax, bx + 1):
            for y in range(ay, by + 1):
                if ay == by:  # horz
                    yield x, ay, inst
                elif ax == bx:  # vert
                    yield ax, y, inst
                else:  # diag
                    yield x, y, inst


def count(grid: Grid) -> int:
    total = 0
    for x in range(1000):
        for y in range(1000):
            total += grid[x][y]
    return total


@asserter
def part1(lines: list[str]) -> int:
    grid = new_grid()

    def change_light(x: int, y: int, inst: int) -> None:
        if inst == 1:
            v = 1
        elif inst == 2:
            v = 0
        else:
            v = 1 - grid[x][y]
        grid[x][y] = v

    for x, y, inst in parse(lines):
        change_light(x, y, inst)

    return count(grid)


@asserter
def part2(lines: list[str]) -> int:
    grid = new_grid()

    def change_brightness(x: int, y: int, inst: int) -> None:
        v = grid[x][y]
        if inst == 1:
            v += 1
        elif inst == 2:
            v -= 1
            v = 0 if v < 0 else v
        else:
            v += 2
        grid[x][y] = v

    for x, y, inst in parse(lines):
        change_brightness(x, y, inst)

    return count(grid)


@timing("day6")
def main() -> int:
    i = InputReader(2015, 6).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(
            [
                "turn on 0,0 through 999,999",
                "toggle 0,0 through 999,0",
                "turn off 499,499 through 500,500",
            ]
        )(998996)
        assert part1(puzzle)(377891)

    def s2() -> None:
        assert part2(["turn on 0,0 through 0,0", "toggle 0,0 through 999,999"])(2000001)
        assert part2(puzzle)(14110788)

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
