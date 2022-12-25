import collections

from dash.dash import re

from support import Point  # type: ignore
from support import Directions, check_result, read_file_raw, timing

RE_DIRECTIONS = re.compile(r"([0-9]+)([RL])?")


def parse_input(input: str):
    walls = set()
    empty = set()
    maze, path = input.split("\n\n")
    for y, row in enumerate(maze.splitlines()):
        for x, p in enumerate(row):
            if p == ".":
                empty.add(Point(x, y))
            elif p == "#":
                walls.add(Point(x, y))

    print(max(x, y) + 1)

    return walls, empty, path


@timing("part1")
def part1(input: str) -> int:
    dirs: list[tuple[int, int]] = [
        Directions.RIGHT,
        Directions.DOWN,
        Directions.LEFT,
        Directions.UP,
    ]

    blocked, empty, path = parse_input(input)

    grid = empty | blocked

    min_y = 0
    min_x = min(x for x, y in empty if y == min_y)
    pos = Point(min_x, min_y)

    # TODO: drop deque
    curr_dir = collections.deque(list(range(len(dirs))))

    for m in RE_DIRECTIONS.finditer(path):
        i_s, d = m.groups()
        distance = int(i_s)

        t = dirs[curr_dir[0]]

        for _ in range(distance):
            next = pos.x + t[0], pos.y + t[1]

            # wrapping
            if next not in grid:
                match t:
                    case Directions.RIGHT:
                        next = (min(ex for ex, ey in grid if ey == pos.y), pos.y)
                    case Directions.DOWN:
                        next = (pos.x, min(ey for ex, ey in grid if ex == pos.x))
                    case Directions.LEFT:
                        next = (max(ex for ex, ey in grid if ey == pos.y), pos.y)
                    case Directions.UP:
                        next = (pos.x, max(ey for ex, ey in grid if ex == pos.x))
                    case _:
                        raise AssertionError("unreachable")

            if next in blocked:
                # can't move to next position because of a wall
                break
            else:
                pos = Point(*next)

        if d is None:
            break

        # change direction
        if d == "R":
            curr_dir.rotate(-1)
        elif d == "L":
            curr_dir.rotate(1)

    return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + curr_dir[0]


@timing("part2")
def part2(input: str) -> int:
    return 0


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/22/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/22/puzzle.input")

    check_result(6032, part1(sample))
    check_result(50412, part1(puzzle))

    #  check_result(0, part2(sample))
    #  check_result(0, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
