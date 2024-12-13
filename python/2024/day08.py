import sys

from support import Grid, InputReader, P, asserter


def dist(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int]:
    return (x1 - x2), (y1 - y2)


def find_antinodes(g: Grid, *, find_all: bool = False) -> int:
    todo = [*g.grid]
    antinodes: set[P] = set()

    def check(p: P, d: P) -> None:
        (x, y) = p
        (dx, dy) = d
        i = 0
        while g.in_bounds(x, y):
            if find_all or (not find_all and i == 1):
                antinodes.add((x, y))
            x += dx
            y += dy
            i += 1

    while todo:
        a1 = todo.pop()
        for a2 in todo:
            # only if antennas type match
            if g.grid[a2] == g.grid[a1]:
                (dx, dy) = dist(*a1, *a2)
                check(a1, (dx, dy))
                check(a2, (-dx, -dy))

    return len(antinodes)


@asserter
def part1(g: Grid) -> int:
    return find_antinodes(g)


@asserter
def part2(g: Grid) -> int:
    return find_antinodes(g, find_all=True)


def main() -> int:
    i = InputReader(2024, 8).grid

    example = i("example", filter=(".",))
    puzzle = i("puzzle", filter=(".",))

    def s1() -> None:
        assert part1(example)(14)
        assert part1(puzzle)(311)
        # 303 too low

    def s2() -> None:
        assert part2(example)(34)
        assert part2(puzzle)(1115)

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
