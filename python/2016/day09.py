import sys

from support import InputReader, asserter, timing


def decompress(input: str, part: int = 1):
    i = 0
    total = 0
    inside = False
    marker: list[str] = []

    while i < len(input):
        c = input[i]
        if c == "(":
            inside = True
        elif c == ")":
            inside = False
            length, repeat = map(int, "".join(marker).split("x"))
            marker.clear()
            subsequent = input[1 + i : 1 + i + length]
            result = len(subsequent)
            if part == 2:
                result = decompress(subsequent, part)
            total += result * repeat
            i += length
        elif inside:
            marker.append(c)
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
        assert part2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")(445)
        assert part2(puzzle)(10964557606)
        # too low 11577002

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
