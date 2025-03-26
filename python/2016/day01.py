import sys

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    x = y = 0
    dx, dy = (0, 1)
    for dir in input.split(", "):
        if dir[0] == "L":
            dx, dy = dy * -1, dx
        else:
            dx, dy = dy, dx * -1
        n = int(dir[1:])
        if dx == 0:
            y += n * dy
        elif dy == 0:
            x += n * dx
    return abs(x) + abs(y)


@asserter
def part2(input: str) -> int:
    x = y = 0
    dx, dy = (0, 1)
    visited = {(x, y)}
    for dir in input.split(", "):
        if dir[0] == "L":
            dx, dy = dy * -1, dx
        else:
            dx, dy = dy, dx * -1

        for _ in range(int(dir[1:])):
            if dx == 0:
                y += 1 * dy
            elif dy == 0:
                x += 1 * dx
            if (x, y) in visited:
                return abs(x) + abs(y)
            else:
                visited.add((x, y))

    raise AssertionError("unreachable")


@timing("day01")
def main() -> int:
    i = InputReader(2016, 1).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(12)
        assert part1(puzzle)(287)

    def s2() -> None:
        assert part2("R8, R4, R4, R8")(4)
        assert part2(puzzle)(133)

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
