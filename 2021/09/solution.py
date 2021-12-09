from typing import List, Tuple, Union
import os
from support import timing


def parse_input(filename: str) -> List[List[int]]:
    lines: List[List[int]] = []
    path = os.path.dirname(__file__) + "/" + filename
    with open(path, "r") as f:
        for line in f.readlines():
            line = map(lambda x: int(x), line.rstrip())
            lines.append([*line])
    return lines


def find_low_points(areamap: List[List[int]]) -> List[Tuple[int, int, int]]:
    coords: List[Tuple[int, int, int]] = []
    for y, row in enumerate(areamap):
        for x, point in enumerate(row):
            down = areamap[y + 1][x] if y + 1 < len(areamap) else -1
            right = areamap[y][x + 1] if x + 1 < len(row) else -1
            left = areamap[y][x - 1] if x - 1 >= 0 else -1
            up = areamap[y - 1][x] if y - 1 >= 0 else -1
            adjacent = [*filter(lambda x: x != -1, [left, up, right, down])]
            if min(adjacent) > point:
                coords.append((point, x, y))
    return coords


@timing()
def part1(areamap: List[List[int]]) -> int:
    low_point_coords = find_low_points(areamap)
    low_points = [x[0] for x in low_point_coords]
    low_points.append(len(low_points))
    return sum(low_points)


@timing()
def part2_first_attempt(areamap: List[List[int]]):
    low_points_coords = find_low_points(areamap)
    seen_points: List[Tuple[int, int]] = []

    width = len(areamap[0])
    height = len(areamap)

    def is_bounding(x: int, y: int) -> bool:
        return x >= 0 and x < width and y >= 0 and y < height

    def check_point(x: int, y: int) -> Union[Tuple[int, int], None]:
        return (x, y) if is_bounding(x, y) and areamap[y][x] != 9 else None

    def get_adjacent(x: int, y: int) -> List[Union[Tuple[int, int], None]]:
        current = areamap[y][x]
        down = check_point(x, y - 1)
        right = check_point(x + 1, y)
        left = check_point(x - 1, y)
        up = check_point(x, y + 1)
        seen_points.append((x, y))
        down = down if down and current < areamap[down[1]][down[0]] else None
        right = right if right and current < areamap[right[1]][right[0]] else None
        left = left if left and current < areamap[left[1]][left[0]] else None
        up = up if up and current < areamap[up[1]][up[0]] else None
        return [up, right, down, left]

    def compute(x: int, y: int, count: int = 0):
        adjacent = get_adjacent(x, y)
        # skip some on start point
        if len(set(adjacent)) == 2 and count == 0:
            return 0
        count += 1
        for next_point in adjacent:
            if next_point is None:
                continue
            if next_point in seen_points:
                continue
            count = compute(next_point[0], next_point[1], count)
        return count

    basins: List[int] = []
    for (_, x, y) in low_points_coords:
        basins.append(compute(x, y))
    #  print(basins)

    basins = sorted(basins, reverse=True)[:3]
    return basins[0] * basins[1] * basins[2]


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    sample = parse_input("sample.input")
    puzzle = parse_input("puzzle.input")

    check_result(15, part1(sample))
    check_result(564, part1(puzzle))

    check_result(1134, part2_first_attempt(sample))
    check_result(1038240, part2_first_attempt(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
