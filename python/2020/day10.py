import collections

from support import assert_result, read_file_int2, timing


@timing()
def part1(lines: list[int]) -> int:
    diffrences: collections.Counter[int] = collections.Counter({3: 1})

    prev = 0
    for current in lines:
        diffrences[current - prev] += 1
        prev = current

    return diffrences[1] * diffrences[3]


TRIBONACCI = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
}


@timing()
def part2(lines: list[int]) -> int:
    count = 1
    continuous = 0

    prev = 0
    for current in lines:
        if current == prev + 1:
            continuous += 1
        elif continuous > 0:
            count *= TRIBONACCI[continuous]
            # reset
            continuous = 0

        prev = current

    if continuous > 0:
        count *= TRIBONACCI[continuous]

    return count


def main() -> int:
    sample1 = sorted(read_file_int2(__file__, "../../input/2020/10/sample1.input"))
    sample2 = sorted(read_file_int2(__file__, "../../input/2020/10/sample2.input"))
    puzzle = sorted(read_file_int2(__file__, "../../input/2020/10/puzzle.input"))

    assert_result(35, part1(sample1))
    assert_result(220, part1(sample2))
    assert_result(2760, part1(puzzle))

    assert_result(8, part2(sample1))
    assert_result(19208, part2(sample2))
    assert_result(13816758796288, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
