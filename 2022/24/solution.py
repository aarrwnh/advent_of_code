import collections
import math
from typing import Callable

from support import check_result
from support import Directions, Point, read_file_raw, timing

DIRS = {
    "^": Directions.S,
    "v": Directions.N,
    "<": Directions.W,
    ">": Directions.E,
}


class Blizzard:
    def __init__(self, d: str, x: int, y: int) -> None:
        self.direction = d
        self.x = x
        self.y = y

    def move_by(self, x: int, y: int) -> tuple[int, int]:
        return (self.x + x, self.y + y)

    def shift(self, walls: set[Point], max_x: int, max_y: int) -> None:
        self.x, self.y = self.move_by(*DIRS[self.direction])
        # reset blizzard position after reaching wall
        if (self.x, self.y) in walls:
            match self.direction:
                case "^":
                    self.y = max_y
                case "v":
                    self.y = 1
                case ">":
                    self.x = 1
                case "<":
                    self.x = max_x


def parse_grid(input: str) -> tuple[dict[Point, list[Blizzard]], set[Point]]:
    coords: dict[Point, list[Blizzard]] = collections.defaultdict(list)
    walls: set[Point] = set()
    for y, row in enumerate(input.splitlines()):
        for x, p in enumerate(row):
            xy = Point(x, y)
            if p == "#":
                walls.add(xy)
            elif p != ".":
                coords[xy].append(Blizzard(p, x, y))

    return coords, walls


def make_grid_states(
    lcm: int,
    coords: dict[Point, list[Blizzard]],
    walls: set[Point],
    max_x: int,
    max_y: int,
) -> list[set[Point]]:
    states: list[set[Point]] = []
    for _ in range(lcm):
        states.append(set(coords.keys()))
        next_state: dict[Point, list[Blizzard]]
        # use list to keep multiple blizzards on one point
        next_state = collections.defaultdict(list)
        for xy in coords:
            for p in coords[xy]:
                p.shift(walls, max_x - 1, max_y - 1)
                next_state[Point(p.x, p.y)].append(p)
        coords = next_state
    return states


def trip_planner(input: str) -> tuple[Callable[[int, Point, Point], int], Point, Point]:
    coords, walls = parse_grid(input)
    max_wall = max(walls)
    max_x = max_wall.x
    max_y = max_wall.y
    lcm = math.lcm(max_x - 1, max_y - 1)

    all_blizzard_states = make_grid_states(lcm, coords, walls, max_x, max_y)

    possible: list[tuple[int, int]]
    possible = [(0, 0)] + [x for x in DIRS.values()]

    def start_trip(total_time: int, start: Point, end: Point) -> int:
        start_pos = (start.x, start.y, total_time)
        seen: dict[tuple[int, ...], int] = {start_pos: 0}
        todo: collections.deque[tuple[int, ...]]
        todo = collections.deque([start_pos])
        while todo:
            x, y, time = todo.popleft()
            ntime = (time + 1) % lcm

            for dx, dy in possible:
                nx, ny = x + dx, y + dy
                if (
                    (nx, ny, ntime) not in seen
                    and 0 <= nx <= max_x
                    and 0 <= ny <= max_y
                    and (nx, ny) not in walls
                    and (nx, ny) not in all_blizzard_states[ntime]
                ):
                    n = seen[x, y, time] + 1
                    if (nx, ny) == end:
                        return total_time + n
                    seen[(nx, ny, ntime)] = n
                    todo.append((nx, ny, ntime))

        raise AssertionError("unreachable")

    start = Point(1, 0)
    end = Point(max_wall.x - 1, max_wall.y)
    return start_trip, start, end


@timing("part1")
def part1(input: str) -> int:
    make_trip, start_point, end_point = trip_planner(input)
    return make_trip(0, start_point, end_point)


@timing("part2")
def part2(input: str) -> int:
    make_trip, start, end = trip_planner(input)
    trip1 = make_trip(0, start, end)
    trip2 = make_trip(trip1, end, start)
    trip3 = make_trip(trip2, start, end)
    return trip3


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/24/sample")
    puzzle = read_file_raw(__file__, "../../input/2022/24/puzzle")

    check_result(18, part1(sample))
    check_result(322, part1(puzzle))

    check_result(54, part2(sample))
    check_result(974, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
