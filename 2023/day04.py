import collections
from typing import Generator

from support import check_result, read_file_lines, timing


def parse(lines: list[str]) -> Generator[tuple[set[str], set[str]], None, None]:
    for line in lines:
        _, l_s = line.split(":")
        left_s, right_s = l_s.replace("  ", " ").strip().split(" | ")
        winning = set(left_s.split(" "))
        got = set(right_s.split(" "))
        yield winning, got


@timing("part1")
def part1(lines: list[str]) -> int:
    total = 0
    for won, got in parse(lines):
        matches = won.intersection(got)
        if len(matches) > 0:
            total += 1 << len(matches) - 1
    return total


@timing("part2")
def part2(lines: list[str]) -> int:
    inst: collections.defaultdict[int, int]
    inst = collections.defaultdict(int)
    for i, (won, got) in enumerate(parse(lines)):
        matches = len(won.intersection(got))
        inst[i] += 1  # original card
        for j in range(1 + i, 1 + i + matches):
            inst[j] += inst[i]
    return sum(inst.values())


def main() -> int:
    sample = read_file_lines(__file__, "../input/2023/04/sample")
    puzzle = read_file_lines(__file__, "../input/2023/04/puzzle")

    check_result(13, part1(sample))
    check_result(17803, part1(puzzle))

    check_result(30, part2(sample))
    check_result(5554894, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
