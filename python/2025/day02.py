import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


def parse(input: str) -> Generator[int]:
    for line in input.split(","):
        r1, r2 = map(int, line.split("-"))
        for r in range(r1, r2 + 1):
            yield r


def valid1(num: int) -> bool:
    # mi = (math.log10(num) + 1) // 2
    # m = math.pow(10, mi)
    # lo = num % m
    # hi = num // m
    # return lo != hi
    n = str(num)
    if len(n) % 2 != 0:
        return True
    mi = len(n) // 2
    return n[:mi] != n[mi:]


def valid2(num: int) -> bool:
    n = str(num)
    l = len(n)
    mi = l // 2

    for i in range(1, mi + 1):
        if l % i != 0:
            continue

        chunk = n[:i]
        for j in range(1, l // i):
            s = j * i
            if n[s:s + i] != chunk:
                break
        else:
            return False

    return True


@asserter
def part1(input: str) -> int:
    return sum(r for r in parse(input) if not valid1(r))


@asserter
def part2(input: str) -> int:
    return sum(r for r in parse(input) if not valid2(r))


@timing("day2")
def main() -> int:
    i = InputReader(2025, 2).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(1227775554)
        assert part1(puzzle)(19386344315)

    def s2() -> None:
        assert part2(example)(4174379265)
        assert part2(puzzle)(34421651192)

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
