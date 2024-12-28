import sys

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    sch = input.split("\n\n")

    locks: list[list[int]] = []
    keys: list[list[int]] = []

    m = sch[0].splitlines()
    width, height = len(m[0]), len(m)

    for pin in sch:
        lines = pin.splitlines()
        heights = [0] * width
        if lines[0][0] == "#":
            locks.append(heights)
            c = 0
            r = range(height - 1, -1, -1)
        else:
            keys.append(heights)
            c = height - 1
            r = range(height)

        for x in range(width):
            for y in r:
                if lines[y][x] == "#":
                    heights[x] = abs(y - c)
                    break

    total = 0
    for lock in locks:
        for key in keys:
            if not any(a + b > width for a, b in zip(lock, key, strict=True)):
                total += 1
    return total


@timing("day25")
def main() -> int:
    i = InputReader(2024, 25).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(3)
        assert part1(puzzle)(3356)

    match sys.argv:
        case [_, "1"]:
            s1()
        case _:
            s1()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
