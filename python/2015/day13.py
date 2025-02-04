import itertools
import sys
from collections import defaultdict

from support import InputReader, asserter, timing

type Guests = dict[str, dict[str, int]]


def parse(lines: list[str]) -> Guests:
    guests: defaultdict[str, dict[str, int]] = defaultdict(dict)
    for line in lines:
        name1, _, op, amount, *_, name2 = line.rstrip(".").split()
        guests[name1][name2] = int(amount) * (-1 if op == "lose" else 1)
    return guests


def calc_optimal(guests: Guests) -> int:
    keys = list(guests.keys())
    last = keys.pop()
    size = len(guests)
    optimal = 0
    visited = set()
    for indicies in itertools.permutations(range(size - 1)):
        no_edges = indicies[1:-1]
        if no_edges in visited:
            continue
        visited.add(no_edges)
        b = 0
        seating = [keys[i] for i in indicies] + [last]
        for i, g in enumerate(seating):
            b += guests[g][seating[i - 1]]
            b += guests[g][seating[(i + 1) % size]]
        optimal = max(optimal, b)
    return optimal


@asserter
def part1(lines: list[str]) -> int:
    return calc_optimal(parse(lines))


@asserter
def part2(lines: list[str]) -> int:
    guests = parse(lines)
    for name in list(guests.keys()):
        guests["self"][name] = 0
        guests[name]["self"] = 0

    return calc_optimal(guests)


@timing("day13")
def main() -> int:
    i = InputReader(2015, 13).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(330)
        assert part1(puzzle)(709)

    def s2() -> None:
        assert part2(puzzle)(668)

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
