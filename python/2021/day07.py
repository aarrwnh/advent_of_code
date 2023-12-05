from typing import List, Tuple
import os
import statistics
from support import timing


def read_file(filename: str) -> List[int]:
    path = os.path.dirname(__file__) + "/" + filename
    return [int(n) for n in open(path).readlines()[0].rstrip().split(",")]


@timing()
def part1(positions: List[int]) -> Tuple[int, int]:
    dest = int(statistics.median(positions))
    return (
        dest,
        sum([abs(curr - dest) for curr in positions]),
    )


@timing()
def part2(positions: List[int], part2: bool = False) -> Tuple[int, int]:
    def find_position(n: int) -> int:
        s = []
        for pos in positions:
            num = abs(pos - n)
            s.append(num * (num + 1) // 2)
        return sum(s)

    mean = round(statistics.mean(positions))
    closest_position = find_position(mean)

    direction = 1
    if find_position(mean - 1) < closest_position:
        direction = -1

    while find_position(mean + direction) < closest_position:
        mean += direction
        closest_position = find_position(mean)

    return (mean, closest_position)

    #  return (0, min(find_position(i) for i in range(min(positions), max(positions))))


@timing()
def brute_force(positions: List[int]) -> Tuple[int, int]:
    fuel_usage = {}
    prev_fuel = 0
    for position in range(max(positions)):
        fuel = 0
        fuel_larger = False
        for h in positions:
            fuel += sum([n for n in range(1, abs(h - position) + 1)])
            if prev_fuel != 0 and fuel > prev_fuel:
                fuel_larger = True
                break
        if not fuel_larger:
            prev_fuel = fuel
            fuel_usage[position] = fuel
    return sorted(fuel_usage.items(), key=lambda x: x[1])[0]


def check_result(expected: Tuple[int, int], result: Tuple[int, int]) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    example = [*map(lambda x: int(x), "16,1,2,0,4,2,7,1,2,14".split(","))]
    puzzle = read_file("puzzle.input")

    check_result((2, 37), part1(example))
    check_result((350, 345035), part1(puzzle))

    check_result((5, 168), part2(example))
    check_result((478, 97038163), part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
