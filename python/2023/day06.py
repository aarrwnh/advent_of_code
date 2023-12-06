import math
import re

from support import check_result, read_file_raw, timing


def race(time: int, dist: int) -> int:
    # travel_dist = hold_time * (time - hold_time)
    # hold_time * travel_dist > dist
    a = -1
    s = math.sqrt((time ** 2) - 4 * a * -dist)
    x = math.ceil((-time + s) / 2 * a)
    y = math.floor((-time - s) / 2 * a)

    x = x + 1 if x * (time - x) == dist else x
    y = y - 1 if y * (time - y) == dist else y

    return (y - x) + 1


def brute_race(time: int, dist: int) -> int:
    speed = 0
    e = 0
    matches = 0
    while e < time:
        if speed * (time - e) > dist:
            matches += 1
        speed += 1
        e += 1
    return matches


def parse(input: str) -> tuple[list[str], list[str]]:
    a = re.findall(r"([\d]+)", input)
    h = len(a) // 2
    return a[:h], a[h:]


@timing("part1")
def part1(input: str) -> int:
    total = 1
    a, b = parse(input)
    for t, d in zip(map(int, a), map(int, b)):
        total *= race(t, d)
    return total


@timing("part2")
def part2(input: str) -> int:
    a, b = parse(input)
    return race(int("".join(a)), int("".join(b)))


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2023/06/sample")
    puzzle = read_file_raw(__file__, "../../input/2023/06/puzzle")

    check_result(288, part1(sample))
    check_result(1312850, part1(puzzle))

    check_result(71503, part2(sample))
    check_result(36749103, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
