import sys
from collections.abc import Callable, Generator
from typing import NamedTuple

from support import Grid, InputReader, P, asserter, timing

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Compare(NamedTuple):
    a: P
    b: P


def find_plot(p: P, g: Grid, count_sides: bool = False) -> tuple[int, set[P], int]:
    plot: list[P] = [p]

    i, perimeter, sides = 0, 0, 0
    side_points: list[list[P]] = [[], [], [], []]

    cur_label = g.grid[p]

    while i < len(plot):
        p2 = plot[i]
        x, y = p2
        for dx, dy in DIRS:
            n = x + dx, y + dy
            if g.in_bounds(*n) and g.grid[n] == cur_label:
                if n not in plot:
                    plot.append(n)
                continue

            if count_sides:
                if n[0] == x:
                    if n[1] == y + 1:
                        side_points[DOWN].append(p2)
                    else:
                        side_points[UP].append(p2)
                elif n[0] == x + 1:
                    side_points[RIGHT].append(p2)
                else:
                    side_points[LEFT].append(p2)
            perimeter += 1
        i += 1

    if count_sides:

        def counter(
            idx: int,
            key: Callable[[P], P],
            cb: Callable[[Compare], bool],
        ) -> int:
            sides = 1
            input = sorted(side_points[idx], key=key)
            for a, b in zip(input, input[1:], strict=False):
                if cb(Compare(a, b)):
                    sides += 1
            return sides

        sides = sum(
            [
                counter(
                    UP,
                    lambda p: (p[1], p[0]),
                    lambda _: _.a[1] != _.b[1] or _.a[0] + 1 != _.b[0],
                ),
                counter(
                    DOWN,
                    lambda p: (p[1], p[0]),
                    lambda _: _.a[1] != _.b[1] or _.a[0] + 1 != _.b[0],
                ),
                counter(
                    LEFT,
                    lambda p: (p[0], p[1]),
                    lambda _: _.a[0] != _.b[0] or _.a[1] + 1 != _.b[1],
                ),
                counter(
                    RIGHT,
                    lambda p: (p[0], p[1]),
                    lambda _: _.a[0] != _.b[0] or _.a[1] + 1 != _.b[1],
                ),
            ]
        )

    return perimeter, set(plot), sides


def run(
    g: Grid, count_sides: bool = False
) -> Generator[tuple[int, set[P], int], None, None]:
    visited: set[P] = set()
    for p in g.grid:
        if p in visited:
            continue
        perimeter, plot, sides = find_plot(p, g, count_sides)
        visited |= plot
        yield perimeter, plot, sides


@asserter
def part1(g: Grid) -> int:
    return sum(perimeter * len(plot) for perimeter, plot, _ in run(g))


@asserter
def part2(g: Grid) -> int:
    return sum(sides * len(plot) for _, plot, sides in run(g, True))


@timing("day12")
def main() -> int:
    i = InputReader(2024, 12).grid

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(140)
        assert part1(puzzle)(1550156)

    def s2() -> None:
        assert part2(example)(80)
        assert part2(puzzle)(946084)

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
