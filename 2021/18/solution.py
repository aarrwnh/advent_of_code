import math
import re
from typing import Match

from support import check_result, read_file, timing  # type: ignore

RE_PAIR = re.compile(r"\[(\d+),(\d+)\]")
RE_NUM_LEFT = re.compile(r"\d+(?!.*\d)")
RE_NUM_RIGHT = re.compile(r"\d+")


def sub_sum(num1: str):
    def cb(match: Match[str]) -> str:
        return str(int(match[0]) + int(num1))

    return cb


def sub_greater10(match: Match[str]) -> str:
    i = int(match[0])
    return f"[{math.floor(i/2)},{math.ceil(i/2)}]"


def parse_line(line) -> str:
    while True:
        stop = False
        for pair in RE_PAIR.finditer(line):
            before = line[: pair.start()]
            after = line[pair.end() :]

            if before.count("[") - before.count("]") >= 4:
                before = RE_NUM_LEFT.sub(sub_sum(pair[1]), before, count=1)
                after = RE_NUM_RIGHT.sub(sub_sum(pair[2]), after, count=1)
                line = f"{before}0{after}"
                stop = True
                break

        if stop:
            continue

        has_greater = re.search(r"\d{2}", line)
        if has_greater:
            line = re.sub(has_greater[0], sub_greater10, line, count=1)
            continue
        return line


#  @timing()
def part1(lines: list[str]) -> int:
    res = lines[0]
    for line in lines[1:]:
        res = parse_line(f"[{res},{line}]")
    res = parse_line(res)
    return sum_magnitude(res)


@timing()
def part2(lines: list[str]):
    maximum = 0
    for i, line in enumerate(lines):
        for rest in lines[i + 1 :]:
            lr = sum_magnitude(parse_line(f"[{line},{rest}]"))
            rl = sum_magnitude(parse_line(f"[{rest},{line}]"))
            maximum = max(maximum, lr, rl)
    return maximum


def sum_magnitude(input: str) -> int:
    input = eval(input)

    def reduce(v) -> int:
        if isinstance(v, int):
            return v
        else:
            return reduce(v[0]) * 3 + reduce(v[1]) * 2

    return reduce(input)


@timing()
def main() -> int:
    sample1 = read_file(__file__, "sample1.input")
    sample2 = read_file(__file__, "sample2.input")
    puzzle = read_file(__file__, "puzzle.input")

    check_result(143, part1(["[[1, 2], [[3, 4], 5]]"]))
    check_result(1384, part1(["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"]))
    check_result(445, part1(["[[[[1,1],[2,2]],[3,3]],[4,4]]"]))
    check_result(791, part1(["[[[[3,0],[5,3]],[4,4]],[5,5]]"]))
    check_result(1137, part1(["[[[[5,0],[7,4]],[5,5]],[6,6]]"]))
    check_result(3488, part1(sample1))

    check_result(4140, part1(sample2))
    check_result(3691, part1(puzzle))

    check_result(3993, part2(sample2))
    check_result(4756, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
