import sys
from _md5 import md5

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> str:
    seq: list[str] = []
    i = 1_000_000

    while len(seq) != 8:
        b = md5(f"{input}{i}".encode()).digest()
        if b[0] == 0 and b[1] == 0 and b[2] & 0xF0 == 0:
            seq.append(to_string(b[2] & 0xF))
        i += 1

    return "".join(seq)


@asserter
def part2(input: str) -> str:
    seq = [""] * 8
    i = 1_000_000
    count = 0

    while count != 8:
        b = md5(f"{input}{i}".encode()).digest()
        if b[0] == 0 and b[1] == 0 and b[2] & 0xF0 == 0:
            idx = b[2] & 0xF
            if idx < 8 and seq[idx] == "":
                seq[idx] = to_string((b[3] & 0xF0) >> 4)
                count += 1
        i += 1

    return "".join(seq)


def to_string(n: int) -> str:
    if n < 10:
        return chr(ord("0") + n)
    return chr(ord("a") + n - 10)


@timing("day05")
def main() -> int:
    i = InputReader(2016, 5).raw

    example = i("example").strip()
    puzzle = i("puzzle").strip()

    def s1() -> None:
        assert part1(example)("18f47a30")
        assert part1(puzzle)("4543c154")

    def s2() -> None:
        assert part2(example)("05ace8e3")
        assert part2(puzzle)("1050cbbd")

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
