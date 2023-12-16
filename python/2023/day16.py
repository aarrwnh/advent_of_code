import enum
import sys

from support import InputReader, Point, asserter, timing


class Direction(enum.Enum):
    UP = Point(0, -1)  # "^"
    DOWN = Point(0, 1)  # "v"
    LEFT = Point(-1, 0)  # "<"
    RIGHT = Point(1, 0)  # ">"


MIRRORS_MAP = {
    ".": [
        (Direction.RIGHT, Direction.RIGHT),
        (Direction.DOWN, Direction.DOWN),
        (Direction.UP, Direction.UP),
        (Direction.LEFT, Direction.LEFT),
    ],
    "\\": [
        (Direction.RIGHT, Direction.DOWN),
        (Direction.UP, Direction.LEFT),
        (Direction.DOWN, Direction.RIGHT),
        (Direction.LEFT, Direction.UP),
    ],
    "/": [
        (Direction.RIGHT, Direction.UP),
        (Direction.UP, Direction.RIGHT),
        (Direction.DOWN, Direction.LEFT),
        (Direction.LEFT, Direction.DOWN),
    ],
    "|": [
        (Direction.LEFT, Direction.UP),
        (Direction.LEFT, Direction.DOWN),
        (Direction.RIGHT, Direction.UP),
        (Direction.RIGHT, Direction.DOWN),
        (Direction.DOWN, Direction.DOWN),
        (Direction.UP, Direction.UP),
    ],
    "-": [
        (Direction.LEFT, Direction.LEFT),
        (Direction.RIGHT, Direction.RIGHT),
        (Direction.UP, Direction.LEFT),
        (Direction.UP, Direction.RIGHT),
        (Direction.DOWN, Direction.LEFT),
        (Direction.DOWN, Direction.RIGHT),
    ],
}


class Map:
    def __init__(self, grid_data: tuple[dict[Point, str], int, int, Point]):
        grid, width, height, start = grid_data
        self.grid = grid
        self.width = width
        self.height = height
        self.start = start

    def beam(self, start_dir: Direction, dx: int, dy: int) -> int:
        todo: list[tuple[Direction, Point]]
        todo = [(start_dir, Point(dx, dy))]

        visited: set[tuple[Direction, Point]] = set()
        energized_tiles = set()

        while todo:
            (prev_dir, prev_p) = todo.pop()
            n = prev_p.apply(prev_dir.value)
            if not (0 <= n.x < self.width and 0 <= n.y < self.height):
                continue

            if (prev_dir, n) in visited:
                continue

            visited.add((prev_dir, n))
            energized_tiles.add(n)

            ch = self.grid[n]
            for x in MIRRORS_MAP[ch]:
                if x[0] == prev_dir:
                    todo.insert(0, (x[1], n))

        return len(energized_tiles)


@asserter
@timing("part1")
def part1(input: Map) -> int:
    return input.beam(Direction.RIGHT, -1, 0)


@asserter
@timing("part2")
def part2(input: Map) -> int:
    best = []
    for start_dir, xd, yd in [
        (Direction.DOWN, 0, -1),
        (Direction.LEFT, 0, input.width),
        (Direction.RIGHT, -1, 0),
        (Direction.UP, input.height, 0),
    ]:
        prev_energized = 0
        for j in range(input.height):
            prev_energized = max(
                prev_energized,
                input.beam(start_dir, j if xd == 0 else xd, j if yd == 0 else yd),
            )
        best.append(prev_energized)
    return max(best)


def main() -> int:
    i = InputReader(2023, 16).grid

    sample = Map(i("sample"))
    puzzle = Map(i("puzzle"))

    def s1() -> None:
        part1(sample)(46)
        part1(puzzle)(6740)

    def s2() -> None:
        part2(sample)(51)
        part2(puzzle)(7041)

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
