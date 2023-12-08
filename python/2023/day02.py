from typing import Generator

from support import assert_result, mul, read_file_lines, timing


def parse(line: str) -> Generator[tuple[int, str], None, None]:
    for seq in line.split(": ", 1)[1].split("; "):
        for cube in seq.split(", "):
            c = cube.split(", ")[0].split(" ")
            yield int(c[0]), c[1]


@timing("part1")
def part1(lines: list[str]) -> int:
    limit = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for i, line in enumerate(lines, 1):
        for num, color in parse(line):
            if num > limit["red"] and num > limit[color]:
                break
        else:
            total += i
    return total


@timing("part2")
def part2(lines: list[str]) -> int:
    powers: list[int] = []
    for line in lines:
        water = {"red": 0, "green": 0, "blue": 0}
        for num, color in parse(line):
            water[color] = max(water[color], num)
        powers.append(mul(water.values()))
    return sum(powers)


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2023/02/sample")
    puzzle = read_file_lines(__file__, "../../input/2023/02/puzzle")

    assert_result(8, part1(sample))
    assert_result(2207, part1(puzzle))

    assert_result(2286, part2(sample))
    assert_result(62241, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
