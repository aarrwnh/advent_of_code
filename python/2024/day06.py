import sys

from support import Grid, InputReader, P, asserter, timing

DIRECTIONS: list[P] = [
    (0, -1),  # ^
    (1, 0),  # >
    (0, 1),  # v
    (-1, 0),  # <
]


def walker(g: Grid, *, obstacle: None | P = None) -> set[tuple[int, ...]]:
    visited: set[tuple[int, ...]] = set()
    x, y = g.start_pos
    dir = 0

    # put another obstacle for part2
    o = obstacle is not None

    def move(d: int, x: int, y: int) -> tuple[int, int]:
        dx, dy = DIRECTIONS[d]
        return x + dx, y + dy

    while g.in_bounds(x, y):
        a = (dir if o else 0, x, y)
        if o and a in visited:
            # (part2) we loopin' now
            return set(((0, x, y),))
        visited.add(a)

        nx, ny = move(dir, x, y)

        # (part2) loop dir change if two obstacles are adjacent
        while g.in_bounds(nx, ny) and (
            g.grid[(nx, ny)] == "#" or (o and (nx, ny) == obstacle)
        ):
            dir = (dir + 1) % 4
            nx, ny = move(dir, x, y)

        x, y = nx, ny

    return set() if o else visited


@asserter
@timing("part1")
def part1(g: Grid) -> int:
    return len(walker(g))


@asserter
@timing("part2")
def part2(g: Grid) -> int:
    default_path = walker(g)
    total = 0
    for _, x, y in default_path:
        if g.grid[(x, y)] == "." and len(walker(g, obstacle=(x, y))) == 1:
            total += 1
    return total


def main() -> int:
    i = InputReader(2024, 6).grid

    example = i("example", find_start="^")
    puzzle = i("puzzle", find_start="^")

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
