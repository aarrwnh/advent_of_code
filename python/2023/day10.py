import collections
from enum import Enum

from support import InputReader, Point, asserter, timing

# DIRS = {
#     "S": ((0, -1), (0, 1), (1, 0), (-1, 0)),
#     "|": ((0, 1), (0, -1)),
#     "-": ((-1, 0), (1, 0)),
#     "L": ((0, -1), (1, 0)),
#     "7": ((-1, 0), (0, 1)),
#     "F": ((0, 1), (1, 0)),
#     "J": ((0, -1), (-1, 0)),
# }


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def translate_next_dir(ch: str, prev_dir: Direction) -> None | Direction:
    match prev_dir:
        case Direction.UP:
            match ch:
                case "|":
                    return Direction.UP
                case "7":
                    return Direction.LEFT
                case "F":
                    return Direction.RIGHT

        case Direction.RIGHT:
            match ch:
                case "-":
                    return Direction.RIGHT
                case "7":
                    return Direction.DOWN
                case "J":
                    return Direction.UP

        case Direction.DOWN:
            match ch:
                case "|":
                    return Direction.DOWN
                case "J":
                    return Direction.LEFT
                case "L":
                    return Direction.RIGHT

        case Direction.LEFT:
            match ch:
                case "-":
                    return Direction.LEFT
                case "L":
                    return Direction.UP
                case "F":
                    return Direction.DOWN

    return None


def convert_start_char(dirs: list[Direction | None]) -> str:
    match dirs:
        case [None, Direction.DOWN, Direction.LEFT, None]:
            return "F"
        case [None, Direction.UP, Direction.DOWN, None]:
            return "|"
        case [None, Direction.RIGHT, Direction.DOWN, None]:
            return "7"
        case [Direction.LEFT, None, Direction.DOWN, None]:
            return "|"
        case _:
            raise AssertionError("not implemented", dirs)


class Map:
    def __init__(
        self, grid_data: tuple[dict[Point, str], int, int, None | Point]
    ) -> None:
        grid, max_x, max_y, _ = grid_data
        self.max_x = max_x
        self.max_y = max_y
        self.grid = grid
        (start,) = (p for p in grid if grid[p] == "S")
        self.start = start

        # translate S to correct pipe
        a: list[Direction | None] = []
        for _, d, s in [(0, dir, self.start) for dir in Direction]:
            n = Point(s.x + d.value[0], s.y + d.value[1])
            ch = grid.get(n, ".")
            next_dir = translate_next_dir(ch, d)
            a.append(next_dir)
        self.grid[start] = convert_start_char(a)

    def walk_path(self) -> tuple[int, set[Point]]:
        visited: set[Point] = {self.start}
        path: set[Point] = {self.start}

        starting = [(0, dir, self.start) for dir in Direction]
        todo: collections.deque[tuple[int, Direction, Point]]
        todo = collections.deque(starting)

        def try_move(length: int, dir: Direction, curr_p: Point) -> bool:
            n = Point(curr_p.x + dir.value[0], curr_p.y + dir.value[1])
            ch = self.grid.get(n, ".")
            next_dir = translate_next_dir(ch, dir)
            if next_dir is not None:
                path.add(n)
                if n in visited:
                    return False
                visited.add(n)
                todo.append((length + 1, next_dir, n))
            return True

        while todo:
            length, dir, p = todo.popleft()
            if not try_move(length, dir, p):
                return length + 1, path

        raise AssertionError("unreachable")


@asserter
@timing("part1")
def part1(m: Map) -> int:
    return m.walk_path()[0]


@asserter
@timing("part2")
def part2(m: Map) -> int:
    _, visited = m.walk_path()

    count = 0
    inside = False

    # TODO: try flood fill???
    # TODO: make | into 1 and everything else to 0?

    for y in range(m.max_y + 1):
        pipe = " "
        for x in range(m.max_x + 1):
            p = Point(x, y)
            if p in visited:
                ch = m.grid.get(p, " ")
                match ch:
                    # flip on edge pipes
                    case "7" if pipe == "L":
                        inside = not inside
                    case "J" if pipe == "F":
                        inside = not inside
                    # flip on stright
                    case "|":
                        inside = not inside
                    # change last seen pipe
                    case "L" | "F":
                        pipe = ch
                    case "." | "S":
                        raise AssertionError("should be unreachable")

            elif inside:
                # increment on each visited point inside the loop
                count += 1

    return count


def main() -> int:
    i = InputReader(2023, 10)

    sample = Map(i.grid2("sample", find_start="S"))
    sample2 = Map(i.grid2("sample2", find_start="S"))
    sample3 = Map(i.grid2("sample3", find_start="S"))
    puzzle = Map(i.grid2("puzzle", find_start="S"))

    part1(sample)(8)
    part1(puzzle)(6923)

    part2(sample2)(8)
    part2(sample3)(4)
    part2(puzzle)(529)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
