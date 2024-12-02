import collections
import sys

from support import InputReader, asserter, timing

T = list[int]


def parse_input(lines: list[str]) -> tuple[T, ...]:
    a, b = [], []
    for line in lines:
        left, right = line.split("   ")
        a.append(int(left))
        b.append(int(right))
    return a, b


@asserter
@timing("part1")
def part1(left: T, right: T) -> int:
    return sum(abs(a - b) for a, b in zip(sorted(left), sorted(right), strict=True))


@asserter
@timing("part2")
def part2(left: T, right: T) -> int:
    count = collections.Counter(right)
    return sum(v * count[v] for v in left if v in count)


def main() -> int:
    i = InputReader(2024, 1).lines

    example = parse_input(i("example"))
    puzzle = parse_input(i("puzzle"))

    def s1() -> None:
        assert part1(*example)(11)
        assert part1(*puzzle)(1579939)

    def s2() -> None:
        assert part2(*example)(31)
        assert part2(*puzzle)(20351745)

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
