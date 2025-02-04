import sys
from collections.abc import Generator

from support import InputReader, asserter, timing

MESSAGE = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""

def parse() -> Generator[tuple[str, str]]:
    for a in MESSAGE.splitlines():
        k, v = a.split(": ")
        yield k, int(v)


def iter(lines: list[str]) -> Generator[tuple[set[tuple[str, int]], str]]:
    for line in lines:
        _, num, *rest = [a.strip(":,") for a in line.split()]
        c = zip(rest[0::2], rest[1::2], strict=True)
        gifts = {(a, int(b)) for a, b in c}
        yield gifts, int(num)


@asserter
def part1(lines: list[str]) -> int:
    msg: set[tuple[str, int]] = set(x for x in parse())

    for gifts, num in iter(lines):
        if msg & gifts == gifts:
            return num

    raise AssertionError("unreachable")


@asserter
def part2(lines: list[str]) -> int:
    msg: dict[str, int] = {k: v for k, v in parse()}

    s1 = {"cats", "trees"}
    s2 = {"pomeranians", "goldfish"}

    def gift_check(name: str, amount: int) -> bool:
        v = msg[name]
        if name in s1:
            return v < amount
        elif name in s2:
            return v > amount
        return v == amount

    for gifts, num in iter(lines):
        if all(gift_check(name, amount) for name, amount in gifts):
            return num

    raise AssertionError("unreachable")


@timing("day16")
def main() -> int:
    i = InputReader(2015, 16).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(213)

    def s2() -> None:
        assert part2(puzzle)(323)

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
