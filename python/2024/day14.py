import math
import re
import sys

from support import InputReader, asserter, timing


class Robot:
    def __init__(self, x: int, y: int, dx: int, dy: int) -> None:
        # original position:
        self._x = x
        self._y = y
        # position after move:
        self.nx = x
        self.ny = y
        # velocity:
        self.dx = dx
        self.dy = dy

    def move(self, seconds: int, width: int, height: int) -> None:
        self.nx = (self._x + seconds * self.dx) % width
        self.ny = (self._y + seconds * self.dy) % height

    def __repr__(self) -> str:
        return f"p={self._x},{self._y} v={self.dx},{self.dy}"


def parse(input: list[str]) -> list[Robot]:
    r = re.compile("(-?\\d+)")
    robots = []
    for line in input:
        a = [int(a) for a in r.findall(line)]
        robots.append(Robot(*a))
    return robots


@asserter
def part1(lines: list[str], width: int, height: int) -> int:
    robots = parse(lines)

    seconds = 100
    for robot in robots:
        robot.move(seconds, width, height)

    middle_col = width // 2
    middle_row = height // 2
    # x = 0..=4 6..=10
    # y = 0..=3 5..=7

    def cmp(x: int, y: int) -> int:
        return (x >= middle_col) << 1 | (y >= middle_row)

    quadrants = [0] * 4
    for robot in robots:
        x, y = robot.nx, robot.ny
        if x != middle_col and y != middle_row:
            quadrants[cmp(x, y)] += 1

    return math.prod(quadrants)


@asserter
def part2(lines: list[str], width: int, height: int) -> int:
    robots = parse(lines)
    robot_count = len(robots)
    max_cycles = width * height
    middle_row = height // 2
    for sec in range(1, max_cycles):
        # v 51 187 288 389
        # h 86 154 257 360
        if sec % height == middle_row:
            for robot in robots:
                robot.move(sec, width, height)
            points = set((r.nx, r.ny) for r in robots)
            if len(points) == robot_count:
                return sec

    raise AssertionError("unreachable")


@timing("day14")
def main() -> int:
    i = InputReader(2024, 14).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, 11, 7)(12)
        assert part1(puzzle, 101, 103)(218619120)

    def s2() -> None:
        assert part2(puzzle, 101, 103)(7055)

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
