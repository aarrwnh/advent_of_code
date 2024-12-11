import sys

from support import Grid, InputReader, P, asserter, timing

START_HEIGHT = ord("0")
END_HEIGHT = ord("9")


def walker(g: Grid) -> list[list[P]]:
    grid = g.grid
    tops: list[list[P]] = []
    for start in [x for x in grid if grid[x] == START_HEIGHT]:
        top: list[P] = []
        queue = [(START_HEIGHT, start)]
        while queue:
            prev_height, prev_pos = queue.pop()
            if prev_height == END_HEIGHT:
                top.append(prev_pos)
                continue

            (x, y) = prev_pos
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if abs(dx) == abs(dy):
                        continue
                    (nx, ny) = (x + dx, y + dy)
                    if g.in_bounds(nx, ny) and grid[(nx, ny)] - prev_height == 1:
                        queue.append((grid[(nx, ny)], (nx, ny)))

        tops.append(top)
    return tops


@asserter
def part1(g: Grid) -> int:
    return sum(len(set(top)) for top in walker(g))


@asserter
def part2(g: Grid) -> int:
    return sum(len(top) for top in walker(g))


@timing("day10")
def main() -> int:
    i = InputReader(2024, 10).grid

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(36)
        assert part1(puzzle)(510)

    def s2() -> None:
        assert part2(example)(81)
        assert part2(puzzle)(1058)

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
