import sys

from support import InputReader, asserter, timing


def parse_input(lines: list[str]) -> tuple[list[int], ...]:
    a: list[int] = []
    b: list[int] = []
    for line in lines:
        left, *right = line.split(" ")
        a.append(int(left.strip()))
        b.append(int(right[-1].strip()))
    return a, b


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    left, right = parse_input(lines)
    right = sorted(right)
    dist = 0
    for i, val in enumerate(sorted(left)):
        dist += abs(val - right[i])
    return dist


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    score = 0
    count: dict[int, int] = {}
    left, right = parse_input(lines)
    for val in right:
        if val in count:
            count[val] += 1
        else:
            count[val] = 1
    for val in left:
        if val in count:
            score += val * count[val]
    return score


def main() -> int:
    i = InputReader(2024, 1).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(11)
        assert part1(puzzle)(1579939)

    def s2() -> None:
        assert part2(sample)(31)
        assert part2(puzzle)(20351745)

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
