import sys

from support import InputReader, asserter, timing


@asserter
def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        b = False
        inside = 0
        outside = 0
        for i in range(1, len(line) - 2):
            if inside > 0:
                break
            elif line[i] == "[":
                b = True
            elif line[i] == "]":
                b = False
            elif line[i + 1] == line[i] != line[i - 1] == line[i + 2]:
                if not b:
                    outside += 1
                else:
                    inside += 1

        if inside == 0 and outside > 0:
            total += 1

    return total


@asserter
def part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        b = False
        inside: set[tuple[str, str]] = set()
        outside: set[tuple[str, str]] = set()
        for i in range(1, len(line) - 1):
            if line[i] == "[":
                b = True
            elif line[i] == "]":
                b = False
            elif line[i] != line[i - 1] == line[i + 1]:
                if not b:
                    outside.add((line[i - 1], line[i]))
                else:
                    inside.add((line[i], line[i + 1]))

        total += len(inside & outside) > 0

    return total


@timing("day7")
def main() -> int:
    i = InputReader(2016, 7).lines

    example = i("example")
    puzzle = i("puzzle")
    example2 = ["aba[bab]xyz", "xyx[xyx]xyx", "aaa[kek]eke", "zazbz[bzb]cdb"]

    def s1() -> None:
        assert part1(example)(2)
        assert part1(puzzle)(105)

    def s2() -> None:
        assert part2(example2)(3)
        assert part2(puzzle)(258)

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
