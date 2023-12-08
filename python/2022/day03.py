from support import assert_result, read_file, timing  # type: ignore


def priority():
    cache: dict[str, int] = {}
    _sa = ord("a") - 1
    _sA = ord("A") - 27

    def get(char: str) -> int:
        if char in cache:
            return cache[char]
        # a-z => 1~26
        # A-Z => 27~52
        cache[char] = ord(char) - (char.islower() and _sa or _sA)
        return cache[char]

    return get


@timing()
def part1(compartments: list[str]) -> int:
    convert_char = priority()
    total = 0
    for rucksack in compartments:
        half = len(rucksack) // 2
        (s,) = set(rucksack[:half]) & set(rucksack[half:])
        total += convert_char(s)
    return total


@timing()
def part2(c: list[str]):
    char_to_int = priority()
    total = 0
    for i in range(0, len(c), 3):
        (char,) = set(c[i]) & set(c[i + 1]) & set(c[i + 2])
        total += char_to_int(char)
    return total


def main() -> int:
    sample = read_file(__file__, "../../input/2022/03/sample.input")
    puzzle = read_file(__file__, "../../input/2022/03/puzzle.input")

    assert_result(157, part1(sample))
    assert_result(7908, part1(puzzle))

    assert_result(70, part2(sample))
    assert_result(2838, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
