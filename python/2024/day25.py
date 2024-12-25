import sys

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    sch = input.split("\n\n")
    pins = []
    for s in sch:
        a = set()
        for y, row in enumerate(s.splitlines()):
            for x, ch in enumerate(row):
                if ch == "#":
                    a.add((x, y))
        pins.append(a)

    total = 0
    for i, pin0 in enumerate(pins):
        for pin1 in pins[i + 1 :]:
            if len(pin0 & pin1) == 0:
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
