from typing import List, NamedTuple, Tuple, Set
import os
from support import timing


class Point(NamedTuple):
    x: int
    y: int


def read_file(filename: str) -> Tuple[Set[Point], List[str]]:
    path = os.path.dirname(__file__) + "/" + filename
    points, folds = open(path, "r").read().split("\n\n")

    return (
        {
            Point(*map(lambda x: int(x), coord.split(",")))
            for coord in points.split("\n")
        },
        [fold for fold in folds.rstrip().split("\n")],
    )


def print_grid(points: Set[Point]) -> str:
    max_x = max(x for x, _ in points) + 1
    max_y = max(y for _, y in points) + 1

    return "\n".join(
        "".join("#" if Point(x, y) in points else " " for x in range(0, max_x)).strip()
        for y in range(0, max_y)
    )


def fold_points(
    fold: Point,
    points: Set[Point],
) -> Set[Point]:
    new_points: Set[Point] = set()
    for point in points:
        if fold.y > 0 and point.y > fold.y:
            y = fold.y - (point.y - fold.y)
            new_points.add(Point(point.x, y))
        elif fold.x > 0 and point.x > fold.x:
            x = fold.x - (point.x - fold.x)
            new_points.add(Point(x, point.y))
        else:
            new_points.add(point)
    return new_points


def compute(
    data: Tuple[Set[Point], List[str]],
    fold_count: int = 0,
) -> Set[Point]:
    points, folds = data

    for idx, fold in enumerate(folds):
        direction, position = fold.split(" ")[2].split("=")
        position = int(position)
        coords = Point(position, 0) if direction == "x" else Point(0, position)
        points = fold_points(coords, points)
        if fold_count and idx == fold_count - 1:
            break

    return points


@timing()
def part1(data: Tuple[Set[Point], List[str]], fold_count: int) -> int:
    return len(compute(data, fold_count))


@timing()
def part2(data: Tuple[Set[Point], List[str]]) -> str:
    return print_grid(compute(data, 0))


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def check_result2(expected: str, result: str) -> None:
    print(result == expected, f"\n\x1b[32m{result}\x1b[0m")


expected_1 = """#####
#   #
#   #
#   #
#####"""

expected_2 = """###   ##  ###  #  #  ##  ###  #  # #
#  # #  # #  # #  # #  # #  # # #  #
#  # #    #  # #### #  # #  # ##   #
###  #    ###  #  # #### ###  # #  #
#    #  # #    #  # #  # # #  # #  #
#     ##  #    #  # #  # #  # #  # ####"""


def main() -> int:
    sample = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    check_result(17, part1(sample, 1))
    check_result(671, part1(puzzle, 1))

    check_result2(expected_1, part2(sample))
    check_result2(expected_2, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
