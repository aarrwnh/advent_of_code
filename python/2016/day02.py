import sys

from support import InputReader, asserter, timing

KEYPAD_1 = [
    "123",
    "456",
    "789",
]

KEYPAD_2 = [
    "  1  ",
    " 234 ",
    "56789",
    " ABC ",
    "  D  ",
]


def simulate(lines: list[str], keypad: list[str]) -> str:
    x, y = None, None
    for i, row in enumerate(keypad):
        for j, ch in enumerate(row):
            if ch == "5":
                x, y = j, i
                break
        else:
            continue
        break

    assert x is not None and y is not None

    num = ""
    size = len(keypad)
    assert size == len(keypad[0])

    for row in lines:
        for dir in row:
            if dir == "L":
                n = x - 1, y
            elif dir == "R":
                n = x + 1, y
            elif dir == "U":
                n = x, y - 1
            else:
                n = x, y + 1
            if 0 <= n[0] < size and 0 <= n[1] < size and keypad[n[1]][n[0]] != " ":
                x, y = n
        num += keypad[y][x]
    return num


@asserter
def part1(directions: list[str]) -> str:
    return simulate(directions, KEYPAD_1)


@asserter
def part2(directions: list[str]) -> str:
    return simulate(directions, KEYPAD_2)


@timing("day02")
def main() -> int:
    i = InputReader(2016, 2).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)("1985")
        assert part1(puzzle)("36629")

    def s2() -> None:
        assert part2(example)("5DB3")
        assert part2(puzzle)("99C3D")

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
