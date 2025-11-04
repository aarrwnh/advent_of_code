import sys

from support import InputReader, asserter, timing


def decompress(input: str, part: int = 1):
    i = 0
    total = 0

    while i < len(input):
        if input[i] == "(":
            j = input.find(")", i)
            marker = input[1 + i : j]
            length, repeats = map(int, "".join(marker).split("x"))
            subsequent = input[1 + j : 1 + j + length]
            result = decompress(subsequent, part) if part == 2 else len(subsequent)
            total += result * repeats
            i = j + length
        else:
            total += 1
        i += 1

    return total


@asserter
def part1(input: str) -> int:
    return decompress(input.strip(), 1)


@asserter
def part2(input: str) -> int:
    return decompress(input.strip(), 2)


@timing("day9")
def main() -> int:
    i = InputReader(2016, 9).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1("X(8x2)(3x3)ABCY")(18)
        assert part1(puzzle)(98135)

    def s2() -> None:
        assert part2(puzzle)(10964557606)

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
