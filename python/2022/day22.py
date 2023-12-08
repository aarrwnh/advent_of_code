import collections
import re

from support import Directions, Point, assert_result, read_file_raw, timing

RE_DIRECTIONS = re.compile(r"([0-9]+)([RL])?")
# right=0 down=1 left=2 up=3
DIRS = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]


def parse_input(
    input: str, tile_size: int = 4
) -> tuple[collections.defaultdict[int, set[Point]], set[Point], str, ]:
    maze, instructions = input.split("\n\n")

    walls = set()
    coords: collections.defaultdict[int, set[Point]]
    coords = collections.defaultdict(set)

    # r_grid = collections.defaultdict(list)

    tile = 0
    for y, row in enumerate(maze.splitlines()):
        j = tile
        for x, p in enumerate(row):
            if p in ".#":
                coords[j].add(Point(x, y))
            if p == "#":
                walls.add(Point(x, y))
            if x % tile_size == 3:
                j += 1
        if y % tile_size == 3:
            # r_grid[j].append(tile)
            tile = j

    return coords, walls, instructions


@timing("part1")
def part1(input: str, tile_size: int) -> int:
    dirs: list[tuple[int, int]] = [
        Directions.RIGHT,
        Directions.DOWN,
        Directions.LEFT,
        Directions.UP,
    ]

    coords, blocked, path = parse_input(input, tile_size)
    grid = set(p for it in coords.values() for p in it)

    min_y = 0
    min_x = min(x for x, y in grid if y == min_y)
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
def part2(input: str, tile_size: int) -> int:
    coords, blocked, instructions = parse_input(input, tile_size)
    grid = set(p for it in coords.values() for p in it)
    pos = min(p for p in grid if p.y == 0)

    direction = 0

    for step in re.split("([RL])", instructions.rstrip()):
        match step:
            case "L":
                direction = (direction + 4 - 1) % 4
            case "R":
                direction = (direction + 1) % 4
            case _:
                for _ in range(0, int(step)):
                    next_pos = pos.add(DIRS[direction])

                    if next_pos in blocked:
                        break

                    if next_pos in grid:
                        pos = next_pos
                    else:
                        # wrap magic
                        current_tile_i = (pos.x // tile_size) + (pos.y // tile_size) * 3
                        (_, new_direction, new_x, new_y) = teleporter(
                            current_tile_i, direction, pos.x, pos.y, tile_size
                        )
                        new_pos = Point(new_x, new_y)
                        if new_pos not in blocked:
                            direction = new_direction
                            pos = new_pos

    # TODO: simulate this someday?
    return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + direction


R = tuple[int, int, int, int]


def teleporter(cur_tile_i: int, direction: int, x: int, y: int, tile_size: int) -> R:
    if tile_size == 50:  # 50x50
        return resolve_size_50(cur_tile_i, direction, x, y)
    if tile_size == 4:
        return resolve_size_4(cur_tile_i, direction, x, y)
    raise AssertionError("tile size not supported")


def resolve_size_4(cur_tile_i: int, direction: int, x: int, y: int) -> R:
    cur_tile = [0, 0, 1, 2, 3, 4, 0, 0, 5, 6][cur_tile_i]
    if cur_tile == 0:
        raise AssertionError("wrong tile")
    match (cur_tile, direction):
        case (1, 0):
            return 6, 1, 8, y + 3
        case (4, 0):
            return 6, 1, x + 3, 8
        case (5, 1):
            return 2, 3, x - 9, 7
        case (3, 3):
            return 1, 0, 8, x - 4
        case _:
            raise AssertionError("unknown wrap")


def resolve_size_50(cur_tile_i: int, direction: int, x: int, y: int) -> R:
    #    ╭─────────╮   ╭─────╮
    #    |       ─────────   |
    #    | ╭─────| 1 | 2 | ╮ |
    #    | |     ───────── | |
    #    | |   ╭─| 3 |─╯   | |
    #    | | ─────────     | |
    #    | ╰─| 4 | 5 |─────╯ |
    #    |   ─────────       |
    #    ╰───| 6 |─╯         |
    #        ─────           |
    #          ╰─────────────╯
    cur_tile = [0, 1, 2, 0, 3, 0, 4, 5, 0, 6][cur_tile_i]
    if cur_tile == 0:
        raise AssertionError("wrong tile")
    match (cur_tile, direction):
        case (1, 3):
            return 6, 0, 0, x + 100
        case (6, 2):
            return 1, 1, y - 100, 0
        case (6, 0):
            return 5, 3, y - 100, 149
        case (5, 1):
            return 6, 2, 49, x + 100
        case (6, 1):
            return 2, 1, x + 100, 0
        case (2, 1):
            return 3, 2, 99, x - 50
        case (3, 0):
            return 2, 3, y + 50, 49
        case (2, 0):
            return 5, 2, 99, 149 - y
        case (5, 0):
            return 2, 2, 149, 149 - y
        case (1, 2):
            return 4, 0, 0, 149 - y
        case (4, 2):
            return 1, 0, 50, 149 - y
        case (4, 3):
            return 3, 0, 50, x + 50
        case (3, 2):
            return 4, 1, y - 50, 100
        case (2, 3):
            return 6, 3, x - 100, 199
        case _:
            raise AssertionError("unknown wrap")


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/22/sample")
    puzzle = read_file_raw(__file__, "../../input/2022/22/puzzle")

    assert_result(6032, part1(sample, 4))
    assert_result(50412, part1(puzzle, 50))

    assert_result(5031, part2(sample, 4))
    assert_result(130068, part2(puzzle, 50))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
