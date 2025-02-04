import sys
from collections.abc import Callable

from support import InputReader, asserter, timing

Coords = set[tuple[int, int]]

DIRS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Lights:
    def __init__(self, lines: list[str]):
        self.coords = self.parse(lines)
        self.width = len(lines[0])
        self.height = len(lines)
        assert self.width == self.height

    def parse(self, lines: list[str]) -> Coords:
        coords: Coords = set()
        for y, row in enumerate(lines):
            for x, ch in enumerate(row):
                if ch == "#":
                    coords.add((x, y))
        return coords

    def count_adjacent(self, x: int, y: int) -> int:
        return sum(True for dx, dy in DIRS if (x + dx, y + dy) in self.coords)

    def step(self):
        new_coords = set()
        for x in range(self.width):
            for y in range(self.height):
                active = self.count_adjacent(x, y)
                if (active in {2, 3} and (x, y) in self.coords) or (
                    active == 3 and (x, y) not in self.coords
                ):
                    new_coords.add((x, y))
        self.coords = new_coords

    def simulate(self, steps: int, cb: Callable[[], None] = lambda: None) -> int:
        for _ in range(steps):
            self.step()
            cb()
        return self.count()

    def count(self) -> int:
        return len(self.coords)


@asserter
def part1(lines: list[str], steps: int) -> int:
    return Lights(lines).simulate(steps)


@asserter
def part2(lines: list[str], steps: int) -> int:
    grid = Lights(lines)

    c = grid.width - 1
    corners = {(0, 0), (c, 0), (0, c), (c, c)}

    def update():
        grid.coords |= corners

    update()
    return grid.simulate(steps, update)


@timing("day18")
def main() -> int:
    i = InputReader(2015, 18).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, 4)(4)
        assert part1(puzzle, 100)(821)

    def s2() -> None:
        assert part2(example, 5)(17)
        assert part2(puzzle, 100)(886)

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
