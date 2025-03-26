import sys
from _md5 import md5

from support import InputReader, asserter, timing


def digest(secret: str, part: int = 1) -> int:
    for i in range(10_000_000):
        key = f"{secret}{i}".encode()
        b = md5(key).digest()
        if b[0] != 0 or b[1] != 0:
            continue
        if part == 1 and b[2] & 0xF0 != 0:
            continue
        if part == 2 and b[2] != 0:
            continue
        return i

        # if b.startswith(startswith): return i
    raise AssertionError("unreachable")


@asserter
def part1(secret: str) -> int:
    return digest(secret, 1)


@asserter
def part2(secret: str) -> int:
    return digest(secret, 2)


@timing("day04")
def main() -> int:
    i = InputReader(2015, 4).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1("abcdef")(609043)
        # assert part1("pqrstuv")(1048970)
        assert part1(puzzle)(346386)

    def s2() -> None:
        assert part2(puzzle)(9958218)

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
