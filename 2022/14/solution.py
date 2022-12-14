from support import fill_points  # type: ignore
from support import Point, check_result, format_coords_hash, read_file_lines, timing


class Sand:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def down(self):
        return self.x, self.y + 1

    def right_down(self):
        return self.x + 1, self.y + 1

    def left_down(self):
        return self.x - 1, self.y + 1

    def reset(self, x: int = 500, y: int = 0):
        self.x = x
        self.y = y

    def update(self, x: int, y: int):
        self.x += x
        self.y += y

    def current(self):
        return Point(self.x, self.y)


def get_wall_coords(lines: list[str]) -> set[Point]:
    walls = set()
    for line in lines:
        coords = line.split(" -> ")
        start = Point.parse(coords.pop())
        while coords:
            next = Point.parse(coords.pop())
            for x in fill_points(start.x, next.x, start.y, next.y):
                walls.add(Point(*x))
            start = next
    return walls


def printer(walls: set[Point], sands: set[Point]) -> None:
    def a(x, y):
        return "o" if (x, y) in sands else "#" if (x, y) in walls else " "

    print(format_coords_hash(walls | sands, cb=a))


@timing("part1")
def part1(lines: list[str], print_final=False) -> int:
    walls = get_wall_coords(lines)
    start = Point(500, 0)
    sand_coords: set[Point] = set()
    bottom_limit = max(y for _, y in walls)
    pos = Sand(*start)

    while True:
        if pos.y > bottom_limit:
            break
        if pos.down() not in walls:
            pos.update(0, 1)
        elif pos.left_down() not in walls:
            pos.update(-1, 1)
        elif pos.right_down() not in walls:
            pos.update(1, 1)
        else:
            sand_coords.add(pos.current())
            # use `walls` for visited points
            walls.add(pos.current())
            pos.reset()

    if print_final:
        printer(walls, sand_coords)

    return len(sand_coords)


@timing("part2")
def part2(lines: list[str], print_final=False):
    walls = get_wall_coords(lines)
    start = Point(500, 0)
    sand_coords: set[Point] = set()
    bottom_limit = max(y for _, y in walls)
    pos = Sand(*start)

    def add(p: Point):
        sand_coords.add(p)
        walls.add(p)
        pos.reset()

    while True:
        # TODO: optimize?
        curr = pos.current()
        if curr in walls:
            break
        elif pos.y > bottom_limit:
            add(curr)
        elif pos.down() not in walls:
            pos.update(0, 1)
        elif pos.left_down() not in walls:
            pos.update(-1, 1)
        elif pos.right_down() not in walls:
            pos.update(1, 1)
        else:
            add(curr)

    if print_final:
        printer(walls, sand_coords)

    return len(sand_coords)


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/14/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/14/puzzle.input")

    check_result(24, part1(sample, True))
    check_result(644, part1(puzzle))

    check_result(93, part2(sample, True))
    check_result(27324, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
