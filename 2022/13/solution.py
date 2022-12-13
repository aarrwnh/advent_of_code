import functools
from ast import literal_eval

from support import check_result, read_file_raw, timing  # type: ignore


def compare(left, right):
    # adjust mixed types first
    if isinstance(left, int) and not isinstance(right, int):
        left = [left]
    elif not isinstance(left, int) and isinstance(right, int):
        right = [right]

    if isinstance(left, list) and isinstance(right, list):
        l_l = len(left)
        l_r = len(right)
        for i in range(min(l_l, l_r) + 1):
            a = left[i] if i < l_l else None
            b = right[i] if i < l_r else None
            #  print(a, b)
            if a is None and b is None:
                continue
            if a is None:
                return -1
            elif b is None:
                return 1
            elif (c := compare(a, b)) != 0:
                return c

    if isinstance(left, int) and isinstance(right, int):
        return left - right

    return 0


@timing()
def part1(input: str) -> int:
    pairs = input.split("\n\n")

    ordered = 0
    for i, pair in enumerate(pairs, 1):
        left, right = pair.splitlines()
        left = literal_eval(left)
        right = literal_eval(right)
        if compare(left, right) <= 0:
            ordered += i

    return ordered


@timing()
def part2(input: str) -> int:
    lines = [literal_eval(x) for x in input.replace("\n\n", "\n").split()]
    dividers = [[[2]], [[6]]]
    lines.extend(dividers)
    lines.sort(key=functools.cmp_to_key(compare))
    return (lines.index(dividers[0]) + 1) * (lines.index(dividers[1]) + 1)


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/13/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/13/puzzle.input")

    check_result(13, part1(sample))
    check_result(5682, part1(puzzle))

    check_result(140, part2(sample))
    check_result(20304, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
