import re

from support import check_result, read_file_lines, timing


@timing("part1")
def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        m = [int(c) for c in line if c.isdigit()]
        total += m[0] * 10 + m[-1]
    return total
    # [line.strip(string.ascii_lowercase) for line in lines]


@timing("part2")
def part2(lines: list[str]) -> int:
    total = 0
    digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    pattern = re.compile("(?=(\\d|" + "|".join(digits) + "))")
    for line in lines:
        m = [
            digits.index(a[1]) + 1 if a[1] in digits else a[1]
            for a in pattern.finditer(line)
        ]
        total += int(m[0]) * 10 + int(m[-1])
    return total


def main() -> int:
    sample1 = read_file_lines(__file__, "../input/2023/01/sample")
    sample2 = read_file_lines(__file__, "../input/2023/01/sample2")
    puzzle = read_file_lines(__file__, "../input/2023/01/puzzle")

    check_result(142, part1(sample1))
    check_result(55607, part1(puzzle))

    check_result(281, part2(sample2))
    check_result(55291, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
