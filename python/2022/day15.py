import re
from typing import NamedTuple

from support import Point  # type: ignore
from support import check_result, make_point_range, read_file_lines, timing


class Sensor(NamedTuple):
    p: Point
    beacon: Point
    dist: int


COORDS = re.compile(r"(?:x|y)=([-0-9]+)")


def parse_lines(lines: list[str]):
    sensors: set[Point] = set()
    beacons: set[Point] = set()
    parsed: list[Sensor] = []

    for line in lines:
        sx, sy, bx, by = (int(x) for x in COORDS.findall(line))
        sensor = Point(sx, sy)
        beacon = Point(bx, by)

        sensors.add(sensor)
        beacons.add(beacon)

        dist = abs(sx - bx) + abs(sy - by)
        parsed.append(Sensor(sensor, beacon, dist))

    return parsed, sensors, beacons


@timing("part1")
def part1(lines: list[str], y: int) -> int:
    covered = set()
    parsed, _, beacons = parse_lines(lines)

    for sensor in parsed:
        sx, sy = sensor.p
        if y in make_point_range(sy - sensor.dist, sy + sensor.dist):
            w = sensor.dist - abs(y - sy)
            covered |= set(make_point_range(sx - w, sx + w))

    return len([x for x in covered if ((x, y) not in beacons)])


@timing("part2")
def part2(lines: list[str], position: int):
    parsed, _, beacons = parse_lines(lines)

    for sensor in parsed:
        top_y = sensor.p.y + sensor.dist - 1
        bottom_y = sensor.p.y - sensor.dist - 1

        for i in range(sensor.dist):
            for x, y in (
                (sensor.p.x + i, top_y - i),
                (sensor.p.x - i, top_y - i),
                (sensor.p.x + i, bottom_y + i),
                (sensor.p.x - i, bottom_y + i),
            ):
                if x < 0 or y < 0 or x > position or y > position:
                    continue
                elif (x, y) in beacons:
                    continue

                for sensor_2 in parsed:
                    if sensor_2.p.dist_to(x, y) <= sensor_2.dist:
                        break
                else:
                    return x * 4000000 + y

    # sample [x = 14, y = 11]
    # puzzle [x = 2662275, y = 3160102]


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/15/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/15/puzzle.input")

    check_result(26, part1(sample, 10))
    check_result(4861076, part1(puzzle, 2000000))

    check_result(56000011, part2(sample, 20))
    check_result(10649103160102, part2(puzzle, 4000000))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
