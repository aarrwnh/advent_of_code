import collections
import sys
from collections.abc import Generator

from support import InputReader, asserter, timing

P = tuple[int, int]

DIRS_DIAGONAL = [
    (1, 1),  # top-right
    (-1, -1),  # bottom-left
    (-1, 1),  # top-left
    (1, -1),  # bottom-right
]

DIRS_ALL = DIRS_DIAGONAL + [
    (0, 1),  # up
    (0, -1),  # down
    (1, 0),  # right
    (-1, 0),  # left
]


def c(x: int, y: int, r: int, dirs: list[P]) -> Generator[P, None, None]:
    for dx, dy in dirs:
        for i in range(1, r):
            yield x + dx * i, y + dy * i
        yield -1, -1  # trigger reset


def parse(lines: list[str]) -> tuple[dict[P, str], int, int]:
    grid: dict[P, str] = {}
    height = len(lines)
    width = len(lines[0].strip())
    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            grid[(x, y)] = p
    return grid, height - 1, width - 1


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    grid, max_y, max_x = parse(lines)

    total = 0

    for x, y in grid:
        if grid[(x, y)] != "X":
            continue
        word = ""
        for dx, dy in c(x, y, 4, DIRS_ALL):
            if dx == -1 and dy == -1:
                if word == "MAS":
                    total += 1
                word = ""
                continue
            if not (0 <= dx <= max_x and 0 <= dy <= max_y):
                continue
            word += grid[(dx, dy)]
    return total


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    grid, max_y, max_x = parse(lines)

    templ = ["A", "S"]
    total = 0
    mas: collections.Counter[P] = collections.Counter()

    for x, y in grid:
        if grid[(x, y)] != "M":
            continue
        found: list[P] = []
        for dx, dy in c(x, y, 3, DIRS_DIAGONAL):
            if dx == -1 and dy == -1:
                if templ == [grid[w] for w in found]:
                    p = found[0]
                    mas[p] += 1
                    if mas[p] == 2 and grid[p] == "A":
                        total += 1
                found.clear()
                continue
            if not (0 <= dx <= max_x and 0 <= dy <= max_y):
                continue
            found.append((dx, dy))
    return total


def main() -> int:
    i = InputReader(2024, 4).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(18)
        assert part1(puzzle)(2336)

    def s2() -> None:
        assert part2(example)(9)
        assert part2(puzzle)(1831)

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