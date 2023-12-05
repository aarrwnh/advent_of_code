import collections
from typing import Generator

from support import check_result, read_file_lines, timing


def parse(lines: list[str]) -> Generator[int, None, None]:
    for line in lines:
        _, l_s = line.split(":")
        left_s, right_s = l_s.replace("  ", " ").strip().split(" | ")
        winning = set(left_s.split(" "))
        have = set(right_s.split(" "))
        matches = winning.intersection(have)
        yield len(matches)


@timing("part1")
def part1(lines: list[str]) -> int:
    return sum(1 << count - 1 for count in parse(lines) if count > 0)


@timing("part2")
def part2(lines: list[str]) -> int:
    inst: collections.defaultdict[int, int]
    inst = collections.defaultdict(int)
    for i, count in enumerate(parse(lines)):
        inst[i] += 1  # original card
        for j in range(1 + i, 1 + i + count):
            inst[j] += inst[i]
    return sum(inst.values())


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2023/04/sample")
    puzzle = read_file_lines(__file__, "../../input/2023/04/puzzle")

    check_result(13, part1(sample))
    check_result(17803, part1(puzzle))

    check_result(30, part2(sample))
    check_result(5554894, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
