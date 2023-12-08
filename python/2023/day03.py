from support import adjacents_bounds, assert_result, read_file_lines, timing

Point = tuple[int, int]
Parsed = list[tuple[int, set[Point]]]


@timing("parse")
def parse(lines: list[str]) -> tuple[dict[Point, str], Parsed]:
    symbols: dict[Point, str] = {}
    parsed: Parsed = []
    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1

    for y, row in enumerate(lines):
        num = 0
        points = set()
        for x, p in enumerate(row + "."):
            if p.isdigit():
                num = num * 10 + int(p)
                for pd in adjacents_bounds(x, y, max_x, max_y, diagonals=True):
                    if pd not in points:
                        points.add(pd)
            else:
                if num > 0:
                    parsed.append((num, points.copy()))
                    num = 0
                    points.clear()
                if p != ".":
                    symbols[(x, y)] = p
    return symbols, parsed


@timing("part1")
def part1(symbols: dict[Point, str], parsed: Parsed) -> int:
    total = 0
    for n, p in parsed:
        if len(p.intersection(symbols)) > 0:
            total += n
    return total


@timing("part2")
def part2(symbols: dict[Point, str], parsed: Parsed) -> int:
    total = 0
    for g, symbol in symbols.items():
        if symbol != "*":
            continue
        a = [n for (n, p) in parsed if g in p]
        if len(a) == 2:
            total += a[0] * a[1]
    return total


@timing("total")
def main() -> int:
    sample = parse(read_file_lines(__file__, "../../input/2023/03/sample"))
    puzzle = parse(read_file_lines(__file__, "../../input/2023/03/puzzle"))

    assert_result(4361, part1(*sample))
    assert_result(546312, part1(*puzzle))

    assert_result(467835, part2(*sample))
    assert_result(87449461, part2(*puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
