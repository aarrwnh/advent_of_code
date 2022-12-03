from support import check_result, read_file, timing  # type: ignore


def priority():
    cache: dict[str, int] = {}

    def get(char: str) -> int:
        if char in cache:
            return cache[char]
        i = ord(char)
        # a-z => 1~26
        if i >= 97 and i <= 122:
            cache[char] = i - 96
        # A-Z => 27~52
        elif i >= 65 and i <= 90:
            cache[char] = i - 38
        return cache[char]

    return get


@timing()
def part1(compartments: list[str]) -> int:
    convert_char = priority()
    total = 0
    for rucksack in compartments:
        half = len(rucksack) // 2
        first, second = rucksack[:half], rucksack[half:]
        for char in first:
            count1 = first.count(char)
            count2 = second.count(char)
            if count2 == 0:
                continue
            if count1 > 0:
                total += convert_char(char)
                break
    return total


@timing()
def part2(compartments: list[str]):
    char_to_int = priority()
    total = 0
    for i in range(0, len(compartments), 3):
        for char in compartments[i]:
            count1 = compartments[i].count(char)
            count2 = compartments[i + 1].count(char)
            if count2 == 0:
                continue
            count3 = compartments[i + 2].count(char)
            if count3 == 0:
                continue
            if count1 > 0:
                total += char_to_int(char)
                break
    return total


def main() -> int:
    sample = read_file(__file__, "../../input/2022/03/sample.input")
    puzzle = read_file(__file__, "../../input/2022/03/puzzle.input")

    check_result(157, part1(sample))
    check_result(7908, part1(puzzle))

    check_result(70, part2(sample))
    check_result(2838, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
