from typing import List, NamedTuple
import os
from support import timing


class Points(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    @staticmethod
    def split(coords: str) -> List[int]:
        x, y = coords.split(",")
        return [int(x), int(y)]

    @classmethod
    def parse(cls, line: str):
        left, right = line.rstrip().split(" -> ")
        return cls(*[*cls.split(left), *cls.split(right)])


def read_file(filename: str) -> List[Points]:
    path = os.path.dirname(__file__) + "/" + filename
    return [Points.parse(line) for line in open(path).readlines()]


def make_point_range(start: int, stop: int):
    is_reverse = -1 if start > stop else 1
    return [*range(start, stop + is_reverse, is_reverse)]
    #  return [*range(min(start, stop), max(start, stop) + 1)]


def fill_points(x1: int, y1: int, x2: int, y2: int, diagonals: bool = False):
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


def create_field(size: int = 10) -> List[List[int]]:
    return [[0 for _ in range(size)] for _ in range(size)]


def print_field(field: List[List[int]]):
    print()
    [print("".join(map(lambda x: str("." if x == 0 else x), i))) for i in field]


def draw_pipes(
    segments: List[Points],
    field_size: int = 10,
    diagonal: bool = False,
    paint: bool = False,
):
    overlaps = 0
    field = create_field(field_size)
    for segment in segments:
        for x, y in fill_points(*segment, diagonal):
            field[y][x] += 1
            if field[y][x] == 2:
                overlaps += 1
    if paint:
        print_field(field)
    return overlaps


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


@timing()
def main() -> int:
    sample = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    check_result(5, draw_pipes(sample, 10, paint=True))
    check_result(12, draw_pipes(sample, 10, diagonal=True, paint=True))

    check_result(3990, draw_pipes(puzzle, 1000))
    check_result(21305, draw_pipes(puzzle, 1000, diagonal=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
