import math
import sys
from collections import defaultdict

from support import InputReader, asserter, timing


def split(num: int) -> tuple[int, ...]:
    if num == 0:
        return (1,)
    f = math.floor(math.log10(num))
    if f % 2 == 1:
        divisor = 10
        while (num / divisor) > divisor:
            divisor *= 10
        return (num // divisor, num % divisor)
    return (num * 2024,)


def blinker(input: str, blinks: int) -> int:
    numbers = [(int(x)) for x in input.split(" ")]

    counter: defaultdict[int, int] = defaultdict(int)
    for x in numbers:
        counter[x] += 1

    for _ in range(blinks):
        nct: defaultdict[int, int] = defaultdict(int)
        for num in counter:
            for x in split(num):
                nct[x] += counter[num]
        counter = nct

    return sum(counter.values())


@asserter
def part1(input: str) -> int:
    return blinker(input, 25)


@asserter
def part2(input: str) -> int:
    return blinker(input, 75)


@timing("day11")
def main() -> int:
    i = InputReader(2024, 11).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(55312)
        assert part1(puzzle)(186996)

    def s2() -> None:
        assert part2(puzzle)(221683913164898)

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
