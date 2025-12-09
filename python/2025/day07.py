import sys
from functools import cache

from support import InputReader, asserter, timing

type P = tuple[int, int]


@asserter
def part1(input: list[str]) -> int:
    start, splitters = parse(input)
    beams = [start]
    splits = 0

    for _ in range(len(input) // 2):
        n: set[P] = set()
        for r, c in beams:
            nr = r + 2
            if (r, c) in splitters:
                n.add((nr, c - 1))
                n.add((nr, c + 1))
                splits += 1
            else:
                n.add((nr, c))
        beams = list(n)

    return splits


@asserter
def part2(input: list[str]) -> int:
    start, splitters = parse(input)
    end = len(input)

    @cache
    def solve(r: int, c: int) -> int:
        if r > end:
            return 1
        nr = r + 2
        if (r, c) in splitters:
            return solve(nr, c - 1) + solve(nr, c + 1)
        return solve(nr, c)

    return solve(*start)

    # import collections
    # beams: collections.defaultdict[P, int]
    # beams = collections.defaultdict(int)
    # beams[start] = 1
    # for _ in range(len(input) // 2):
    #     for (r, c), splits in list(beams.items()):
    #         nr = r + 2
    #         if (r, c) in splitters:
    #             beams[nr, c - 1] += splits
    #             beams[nr, c + 1] += splits
    #         else:
    #             beams[nr, c] += splits
    # return sum(splits for pos, splits in beams.items() if pos[0] == end)


def parse(input: list[str]) -> tuple[P, set[P]]:
    start = None
    splitters: set[P] = set()
    for r, line in enumerate(input):
        for c, ch in enumerate(line):
            if ch == "S":
                start = (r, c)
            elif ch == "^":
                splitters.add((r, c))

    assert start is not None
    return start, splitters


@timing("day7")
def main() -> int:
    i = InputReader(2025, 7).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(21)
        assert part1(puzzle)(1598)

    def s2() -> None:
        assert part2(example)(40)
        assert part2(puzzle)(4509723641302)

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
