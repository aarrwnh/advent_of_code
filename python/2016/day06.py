import collections
import sys

from support import InputReader, asserter, timing


def parse(lines: list[str]) -> list[list[tuple[str, int]]]:
    freq: list[list[tuple[str, int]]] = []
    for i in range(len(lines[0])):
        freq.append(collections.Counter(line[i] for line in lines).most_common())
    return freq


@asserter
def part1(lines: list[str]) -> str:
    return "".join(c[0][0] for c in parse(lines))


@asserter
def part2(lines: list[str]) -> str:
    return "".join(c[-1][0] for c in parse(lines))


@timing("day6")
def main() -> int:
    i = InputReader(2016, 6).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)("easter")
        assert part1(puzzle)("xdkzukcf")

    def s2() -> None:
        assert part2(example)("advent")
        assert part2(puzzle)("cevsgyvd")

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
