import sys

from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    ranges_s, ingred = input.split("\n\n")
    ranges = [tuple(map(int, line.split("-"))) for line in ranges_s.splitlines()]

    fresh = 0
    for x in ingred.splitlines():
        ing = int(x)
        for r1, r2 in ranges:
            if r1 <= ing <= r2:
                fresh += 1
                break

    return fresh


@asserter
def part2(input: str) -> int:
    ranges_s, _ = input.split("\n\n")
    ranges = sorted([tuple(map(int, line.split("-")))
                    for line in ranges_s.splitlines()])
    s = [ranges[0]]
    for r1, r2 in ranges[1:]:
        p_r1, p_r2 = s[-1]
        if (p_r1 <= r1 <= p_r2 or p_r1 <= r2 <= p_r2):
            s[-1] = (min(r1, p_r1), max(r2, p_r2))
        else:
            s.append((r1, r2))

    return sum(abs(r1 - r2) + 1 for r1, r2 in s)


@timing("day5")
def main() -> int:
    i = InputReader(2025, 5).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(3)
        assert part1(puzzle)(661)

    def s2() -> None:
        assert part2(example)(14)
        assert part2(puzzle)(359526404143208)

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
