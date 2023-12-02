from support import check_result, mul, read_file_lines, timing


def get_subsets(line: str) -> list[list[str]]:
    return [
        cube.split(", ")[0].split(" ")
        for seq in line.split(": ", 1)[1].split("; ")
        for cube in seq.split(", ")
    ]


def number_and_color(cube: list[str]) -> tuple[int, str]:
    return int(cube[0]), cube[1]


@timing("part1")
def part1(lines: list[str]) -> int:
    limit = {"red": 12, "green": 13, "blue": 14}
    possible: list[int] = []
    for i, line in enumerate(lines):
        possible.append(i + 1)
        for subset in get_subsets(line):
            num, color = number_and_color(subset)
            if num > limit[color]:
                possible.pop()
                break
    return sum(possible)


@timing("part2")
def part2(lines: list[str]) -> int:
    powers: list[int] = []
    for line in lines:
        water = {"red": 0, "green": 0, "blue": 0}
        for subset in get_subsets(line):
            num, color = number_and_color(subset)
            water[color] = max(water[color], num)
        powers.append(mul(water.values()))
    return sum(powers)


def main() -> int:
    sample = read_file_lines(__file__, "../input/2023/02/sample")
    puzzle = read_file_lines(__file__, "../input/2023/02/puzzle")

    check_result(8, part1(sample))
    check_result(2207, part1(puzzle))

    check_result(2286, part2(sample))
    check_result(62241, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
