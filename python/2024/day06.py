import sys
from collections.abc import Callable

from support import InputReader, asserter, timing

P = tuple[int, int]
A = tuple[dict[P, str], int, int, P]


DIRECTIONS: list[P] = [
    (0, -1),  # ^
    (1, 0),  # >
    (0, 1),  # v
    (-1, 0),  # <
]


def parse_grid(input: str, start_ch: str) -> A:
    grid: dict[P, str] = {}
    start_pos = (0, 0)
    lines = input.strip().split("\n")
    max_y = len(lines) - 1
    max_x = len(lines[0].strip()) - 1
    for y, row in enumerate(lines):
        for x, p in enumerate(row.strip()):
            grid[(x, y)] = p
            if p == start_ch:
                start_pos = (x, y)
    return grid, max_x, max_y, start_pos


def in_bounds(max_x: int, max_y: int) -> Callable[[int, int], bool]:
    def b(x: int, y: int) -> bool:
        return 0 <= x <= max_x and 0 <= y <= max_y

    return b


def default_walk(input: A) -> set[P]:
    grid, max_x, max_y, start = input

    visited: set[P] = set()
    x, y = start
    dir = 0

    b = in_bounds(max_x, max_y)

    while b(x, y):
        visited.add((x, y))

        dx, dy = DIRECTIONS[dir]
        nx, ny = (x + dx, y + dy)

        if b(nx, ny) and grid[(nx, ny)] == "#":
            dir = (dir + 1) % 4
            dx, dy = DIRECTIONS[dir]
            nx, ny = x + dx, y + dy

        x, y = nx, ny

    return visited


@asserter
@timing("part1")
def part1(input: str) -> int:
    g = parse_grid(input, "^")
    return len(default_walk(g))


@asserter
@timing("part2")
def part2(input: str) -> int:
    g = parse_grid(input, "^")
    grid, max_x, max_y, start = g

    b = in_bounds(max_x, max_y)

    def walk(obstacle: P) -> bool:
        visited: set[tuple[int, ...]] = set()
        x, y = start[0], start[1]
        dir = 0

        while b(x, y):
            if (dir, x, y) in visited:
                # we loopin' now
                return True

            visited.add((dir, x, y))
            dx, dy = DIRECTIONS[dir]
            nx, ny = (x + dx, y + dy)

            # loop dir change if two obstacles are adjacent
            while b(nx, ny) and (grid[(nx, ny)] == "#" or (nx, ny) == obstacle):
                dir = (dir + 1) % 4
                dx, dy = DIRECTIONS[dir]
                nx, ny = x + dx, y + dy

            x, y = nx, ny

        return False

    path = default_walk(g)
    return sum([1 for o in path if grid[o] == "." and walk(o)])


def main() -> int:
    i = InputReader(2024, 6).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(41)
        assert part1(puzzle)(4977)

    def s2() -> None:
        assert part2(example)(6)
        assert part2(puzzle)(1729)

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
