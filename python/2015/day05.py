import sys

from support import InputReader, asserter, timing


@asserter
def part1(lines: list[str]) -> int:
    bad_strings = ["ab", "cd", "pq", "xy"]
    vowels = "aieou"
    total = 0
    for line in lines:
        vowel_count = 0
        a = 1
        n = len(line)
        for i in range(n):
            if line[i] in vowels:
                vowel_count += 1
                if vowel_count == 3:
                    a |= 4
            if i < n - 1:
                if line[i] == line[i + 1]:
                    a |= 2
                if f"{line[i]}{line[i + 1]}" in bad_strings:
                    a ^= 1

        # if vowel_count >= 3 and has_double and not has_bad:
        if a >> 1 ^ 3 == 0 and a & 1 == 1:
            total += 1

    return total


@asserter
def part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        a = 0
        n = len(line) - 1
        for i in range(n):
            for j in range(i + 2, n):
                if line[i] == line[j] and line[i + 1] == line[j + 1]:
                    a |= 0b01
                    break
            if i < n - 1 and line[i] == line[i + 2]:
                a |= 0b10

            if a ^ 0b11 == 0:
                total += 1
                break

    return total


@timing("day5")
def main() -> int:
    i = InputReader(2015, 5).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(
            [
                "aaa",
                "ugknbfddgicrmopn",
                "jchzalrnumimnmhp",
                "haegwjzuvuyypxyu",
                "dvszwmarrgswjxmb",
            ]
        )(2)
        assert part1(puzzle)(236)

    def s2() -> None:
        assert part2(
            ["aaa", "qjhvhtzxzqqjkmpb", "xxyxx", "uurcxstgmygtbstg", "ieodomkazucvgmuy"]
        )(2)
        assert part2(puzzle)(51)

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
