#  import collections
import sys
from typing import Generator

from support import assert_result, read_file_raw, timing  # type: ignore


def parse_input(input: str) -> set[tuple[int, int, int]]:
    coords: set[tuple[int, int, int]] = set()
    for line in input.splitlines():
        x, y, z = map(int, line.split(","))
        coords.add((x, y, z))
    return coords


def adjacents(x: int, y: int, z: int) -> Generator[tuple[int, int, int], None, None]:
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


@timing("part1")
def part1(input: str) -> int:
    coords = parse_input(input)
    #  i = len(coords) * 6
    #  for p in coords:
    #      for x_a, y_a, z_a in adjacents(*p):
    #          if (x_a, y_a, z_a) in coords:
    #              i -= 1
    return surface_area(coords)


def surface_area(pts: set[tuple[int, int, int]]) -> int:
    count = 0
    coords = set()
    for pt in pts:
        count += 6
        for cpt in adjacents(*pt):
            # if found in seen points, reduce by 2 -- two sides will merge into nothing
            if cpt in coords:
                count -= 2
        coords.add(pt)
    return count


@timing("part2")
def part2(input: str) -> int:
    coords = parse_input(input)

    min_x = min_y = min_z = sys.maxsize
    max_x = max_y = max_z = -sys.maxsize

    count = len(coords) * 6
    for p in coords:
        x, y, z = p
        for x_a, y_a, z_a in adjacents(*p):
            if (x_a, y_a, z_a) in coords:
                count -= 1

        # find min,max values limiting search area to a "cube" area
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_z = min(min_z, z)
        max_z = max(max_z, z)

    all_outer_coords = {
        (x, y, z)
        for x in range(min_x - 1, max_x + 2)
        for y in range(min_y - 1, max_y + 2)
        for z in range(min_z - 1, max_z + 2)
    }

    remaining = all_outer_coords - coords

    todo = [min(remaining)]
    while todo:
        p = todo.pop()
        if p in remaining:
            remaining.discard(p)
        else:
            continue

        for cpt in adjacents(*p):
            todo.append(cpt)

    return count - surface_area(remaining)


def part22():
    pass


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/18/sample.txt")
    puzzle = read_file_raw(__file__, "../../input/2022/18/puzzle.txt")

    assert_result(64, part1(sample))
    assert_result(3636, part1(puzzle))

    assert_result(58, part2(sample))
    assert_result(2102, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
