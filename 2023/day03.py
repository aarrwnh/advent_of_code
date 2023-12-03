from typing import Generator
from support import check_result, read_file_lines, timing


Point = tuple[int, int]
Parsed = list[tuple[int, set[Point]]]


def adjacents(
    x: int,
    y: int,
    max_x: int,
    max_y: int,
) -> Generator[tuple[int, int], None, None]:
    coords = (-1, 0, 1)
    for x_d in coords:
        for y_d in coords:
            if x_d == y_d == 0:
                continue
            if in_bounds(x + x_d, y + y_d, max_x, max_y):
                yield x + x_d, y + y_d


def in_bounds(x: int, y: int, max_x: int, max_y: int) -> bool:
    return x >= 0 and x < max_x and y >= 0 and y < max_y


@timing("parsing")
def parse(lines: list[str]) -> tuple[set[Point], Parsed]:
    symbols: set[Point] = set()
    parsed: Parsed = []
    max_y = len(lines)
    max_x = len(lines[0])
    for y, row in enumerate(lines):
        num = 0
        points = set()
        for x, p in enumerate(row + "."):
            if p.isdigit():
                num = num * 10 + int(p)
                for pd in adjacents(x, y, max_x, max_y):
                    if pd not in points:
                        points.add(pd)
            else:
                if num > 0:
                    if num in parsed:
                        raise AssertionError("")
                    parsed.append((num, points))
                    num = 0
                    points = set()
                if p != ".":
                    symbols.add((x, y))
    return symbols, parsed


@timing("part1")
def part1(lines: list[str]) -> int:
    total = 0
    symbols, parsed = parse(lines)
    for (n, p) in parsed:
        if len(p.intersection(symbols)) > 0:
            total += n
    return total


@timing("part1")
def part2(lines: list[str]) -> int:
    total = 0
    symbols, parsed = parse(lines)
    gears = [s for s in symbols if lines[s[1]][s[0]] == "*"]
    for g in gears:
        a = [n for (n, p) in parsed if g in p]
        if len(a) > 1:
            total += a[0] * a[1]
    return total


def main() -> int:
    sample = read_file_lines(__file__, "../input/2023/03/sample")
    puzzle = read_file_lines(__file__, "../input/2023/03/puzzle")

    check_result(4361, part1(sample))
    check_result(546312, part1(puzzle))

    check_result(467835, part2(sample))
    check_result(87449461, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
