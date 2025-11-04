import sys

from support import InputReader, asserter, timing


def parse(lines: list[str]) -> list[tuple[int, ...]]:
    return [
        (i, *tuple(int(x) for x in line.replace(".", "").split(" ")[3:12:8]))
        for i, line in enumerate(lines, 1)
    ]


# returns (gcd, x)
def egcd(a: int, n: int) -> tuple[int, int]:
    t, newt = 0, 1
    r, newr = n, a
    while True:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
        if newr == 0:
            break
    return r, t


def solve(discs: list[tuple[int, ...]]) -> int:
    t = 0
    step = 1
    for (disc, positions, pos) in discs:
        gcd, x = egcd(step, positions)
        initial_diff = -(disc + pos + t)
        t += (step * (((initial_diff % positions) * x) % positions)) // gcd
        step = abs(step * positions) // gcd
    return t


@asserter
def part1(lines: list[str]) -> int:
    return solve(parse(lines))


@asserter
def part2(lines: list[str]) -> int:
    states = parse(lines)
    states.append((len(states) + 1, 11, 0))
    return solve(states)


@timing("day15")
def main() -> int:
    i = InputReader(2016, 15).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(5)
        assert part1(puzzle)(122318)

    def s2() -> None:
        assert part2(example)(85)
        assert part2(puzzle)(3208583)

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

# def brute_rotate(states: list[tuple[int, ...]]) -> int:
#     for time in range(10_000_000):
#         for disc, (total, pos) in enumerate(states, 1):
#             if (pos + time + disc) % total == 0:
#                 continue
#             else:
#                 break
#         else:
#             return time
#     raise AssertionError("capsule did not fall")
