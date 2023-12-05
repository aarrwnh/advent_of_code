from support import Point, check_result, make_point_range, read_file_lines, timing


def fill_points_diag(x1: int, y1: int, x2: int, y2: int, diagonals: bool = False):
    x_points = make_point_range(x1, x2)
    y_points = make_point_range(y1, y2)
    len_x = len(x_points)
    len_y = len(y_points)

    if diagonals:
        if len_x > len_y:
            y_points = [y1] * len_x
        elif len_x < len_y:
            x_points = [x1] * len_y
    else:
        if x1 == x2:
            x_points = [x1] * len_y
        elif y1 == y2:
            y_points = [y1] * len_x
        else:
            return []

    if len(x_points) != len(y_points):
        raise AssertionError("x and y are not equal")

    return zip(x_points, y_points)


def create_field(size: int = 10) -> list[list[int]]:
    return [[0 for _ in range(size)] for _ in range(size)]


def print_field(field: list[list[int]]):
    print()
    [print("".join(map(lambda x: str("." if x == 0 else x), i))) for i in field]


def draw_pipes(
    segments: list[list[Point]],
    field_size: int = 10,
    diagonal: bool = False,
    paint: bool = False,
):
    overlaps = 0
    field = create_field(field_size)
    for segment in segments:
        for x, y in fill_points_diag(*segment[0], *segment[1], diagonal):
            #  print("<", x, y)
            field[y][x] += 1
            if field[y][x] == 2:
                overlaps += 1
    if paint:
        print_field(field)
    return overlaps


def parse_input(filename: str) -> list[list[Point]]:
    lines = read_file_lines(__file__, filename)
    return [[Point.parse(s) for s in line.rstrip().split(" -> ")] for line in lines]


@timing()
def main() -> int:
    sample = parse_input("../../input/2021/05/sample.input")
    puzzle = parse_input("../../input/2021/05/puzzle.input")

    check_result(5, draw_pipes(sample, 10, paint=True))
    check_result(3990, draw_pipes(puzzle, 1000))

    check_result(12, draw_pipes(sample, 10, diagonal=True, paint=True))
    check_result(21305, draw_pipes(puzzle, 1000, diagonal=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
