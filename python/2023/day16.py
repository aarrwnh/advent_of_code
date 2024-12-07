import sys

from support import InputReader, Point, asserter, timing


class Grid:
    def __init__(self, grid_data: tuple[dict[Point, str], int, int, Point]):
        grid, width, height, start = grid_data
        self.grid = grid
        self.width = width
        self.height = height
        self.start = start

    def beam(self, start: Point, dir: Point) -> int:
        todo: list[tuple[Point, Point]]
        todo = [(start, dir)]

        visited: set[tuple[int, ...]] = set()
        energized_tiles = set()

        while todo:
            (prev_p, prev_dir) = todo.pop()
            x, y = prev_p.x, prev_p.y
            dx, dy = prev_dir.x, prev_dir.y
            if (x, y, dx, dy) in visited:
                continue
            visited.add((x, y, dx, dy))

            while True:
                if not (0 <= x < self.width and 0 <= y < self.height):
                    break

                ch = self.grid[Point(x, y)]
                energized_tiles.add((x, y))
                match ch:
                    case ".":
                        x += dx
                        y += dy
                    case "\\":
                        todo.insert(0, (Point(x + dy, y + dx), Point(dy, dx)))
                        break
                    case "/":
                        todo.insert(0, (Point(x - dy, y - dx), Point(-dy, -dx)))
                        break
                    case "|":
                        if dx != 0:
                            # split into two beams
                            todo.insert(0, (Point(x, y - 1), Point(0, -1)))
                            todo.insert(0, (Point(x, y + 1), Point(0, 1)))
                            break
                        else:
                            # continue path as .
                            y += dy
                    case "-":
                        if dy != 0:
                            todo.insert(0, (Point(x - 1, y), Point(-1, 0)))
                            todo.insert(0, (Point(x + 1, y), Point(1, 0)))
                            break
                        else:
                            x += dx

        return len(energized_tiles)


@asserter
@timing("part1")
def part1(g: Grid) -> int:
    return g.beam(Point(0, 0), Point(1, 0))


@asserter
@timing("part2")
def part2(g: Grid) -> int:
    best = []
    for x, y, d in [
        (-2, 0, Point(0, 1)),  # DOWN
        (0, -2, Point(1, 0)),  # RIGHT
        (g.width, -2, Point(-1, 0)),  # LEFT
        (-2, g.height - 1, Point(0, -1)),  # UP
    ]:
        prev_energized = 0
        for j in range(g.height):
            start = Point(j if x == -2 else x, j if y == -2 else y)
            prev_energized = max(prev_energized, g.beam(start, d))
        best.append(prev_energized)
    return max(best)


def main() -> int:
    i = InputReader(2023, 16).grid2

    sample = Grid(i("sample"))
    puzzle = Grid(i("puzzle"))

    def s1() -> None:
        assert part1(sample)(46)
        assert part1(puzzle)(6740)

    def s2() -> None:
        assert part2(sample)(51)
        assert part2(puzzle)(7041)

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
