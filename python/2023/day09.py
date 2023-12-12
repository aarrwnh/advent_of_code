from collections.abc import Callable

from support import InputReader, maybe_asserter_chain, timing


def extrapolate(a: list[int], num_pos: int) -> list[int]:
    b: list[int] = []
    n = a
    while True:
        c = [n[i + 1] - n[i] for i in range(len(n) - 1)]
        if c[0] == 0 and c[-1] == 0:
            break
        b.append(c[num_pos])
        n = c
    return b


def parse(lines: list[str], num_pos: int, f: Callable[[int, int], int]) -> int:
    total = 0
    for line in lines:
        a = [int(x) for x in line.split(" ")]
        b = extrapolate(a, num_pos)
        p = 0
        for j in range(len(b) - 1, -1, -1):
            p = f(b[j], p)
        total += f(a[num_pos], p)
    return total


@maybe_asserter_chain
@timing("part1")
def part1(lines: list[str]) -> int:
    return parse(lines, -1, lambda x, y: x + y)


@maybe_asserter_chain
@timing("part2")
def part2(lines: list[str]) -> int:
    return parse(lines, 0, lambda x, y: x - y)
    # or just reverse each line


def main() -> int:
    i = InputReader(2023, 9)

    sample = i.lines("sample")
    puzzle = i.lines("puzzle")

    part1(sample, puzzle)(114, 1877825184)
    part2(sample, puzzle)(2, 1108)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
