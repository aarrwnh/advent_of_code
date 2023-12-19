import sys

from support import InputReader, asserter, timing

DIRS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    x, y = 0, 0
    dx, dy = 1, 0

    for line in lines:
        dir, dist_s = line[0], line[1:]
        dist = int(dist_s)

        match dir:
            case "F":
                x += dx * dist
                y += dy * dist
            case "N":
                y -= dist
            case "S":
                y += dist
            case "E":
                x += dist
            case "W":
                x -= dist
            case "L":
                idx = DIRS.index((dx, dy))
                r = idx + (dist // 90)
                dx, dy = DIRS[r % 4]
            case "R":
                idx = DIRS.index((dx, dy))
                r = idx - (dist // 90)
                dx, dy = DIRS[r % 4]

    return abs(x) + abs(y)


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    x, y = 0, 0
    wx, wy = 10, -1

    for line in lines:
        dir, dist_s = line[0], line[1:]
        dist = int(dist_s)

        match dir:
            case "F":
                x += wx * dist
                y += wy * dist
            case "N":
                wy -= dist
            case "S":
                wy += dist
            case "E":
                wx += dist
            case "W":
                wx -= dist
            case "L":
                for _ in range(dist // 90):
                    wy, wx = wx * -1, wy
            case "R":
                for _ in range(dist // 90):
                    wy, wx = wx, wy * -1

    return abs(x) + abs(y)


def main() -> int:
    i = InputReader(2020, 12).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(25)
        assert part1(puzzle)(1441)

    def s2() -> None:
        assert part2(sample)(286)
        assert part2(puzzle)(61616)

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
