import sys

from support import InputReader, asserter, timing

Towels = tuple[set[str], list[str], int]


def parse(input: str) -> Towels:
    p_s, d_s = input.split("\n\n")
    patterns = set(p_s.split(", "))
    designs = d_s.strip().split("\n")
    max_len = len(max(patterns, key=len))
    return (patterns, designs, max_len)


@asserter
def part1(input: Towels) -> int:
    # @cache
    # def can_match(design: str) -> int:
    #     if len(design) == 0:
    #         return True
    #     for pat in patterns:
    #         if design.startswith(pat) and can_match(design[len(pat):]):
    #             return True
    #     return False

    patterns, designs, max_len = input

    def can_match(design: str) -> bool:
        size = len(design)
        result = [True] + [False] * (size + 1)

        for i in range(1, size + 1):
            for j in range(1, i + 1):
                if j > max_len:
                    break

                if design[i - j : i] in patterns and result[i - j]:
                    result[i] = True
                    break

        return result[size]

    return sum(1 for design in designs if can_match(design) != 0)


@asserter
def part2(input: Towels) -> int:
    # @cache
    # def can_match(design: str) -> int:
    #     if len(design) == 0:
    #         return 1
    #     return sum(
    #         can_match(design[len(pat):]) for pat in patterns if design.startswith(pat)
    #     )

    patterns, designs, max_len = input

    def can_match_count(design: str) -> int:
        size = len(design)
        result = [1] + [0] * (size + 1)

        for i in range(1, size + 1):
            for j in range(1, i + 1):
                if j > max_len:
                    break

                if design[i - j : i] in patterns:
                    result[i] += result[i - j]

        return result[size]

    return sum(can_match_count(design) for design in designs)


@timing("day19")
def main() -> int:
    i = InputReader(2024, 19).raw

    example = parse(i("example"))
    puzzle = parse(i("puzzle"))

    def s1() -> None:
        assert part1(example)(6)
        assert part1(puzzle)(280)

    def s2() -> None:
        assert part2(example)(16)
        assert part2(puzzle)(606411968721181)

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
