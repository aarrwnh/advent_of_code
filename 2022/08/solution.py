from support import check_result, read_file_int, timing


def create_grid(lines: list[list[int]]) -> dict[tuple[int, int], int]:
    grid: dict[tuple[int, int], int] = {}

    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            point = int(p)
            grid[(x, y)] = point

    return grid


@timing()
def part1(lines: list[list[int]]) -> int:
    edge_count = len(lines) * 2 + len(lines[0]) * 2 - 4
    grid = create_grid(lines)

    end_x, end_y = max(grid)
    visible_points = set()

    for x, y in grid:
        # skip on edges
        if x == 0 or y == 0 or x == end_x or y == end_y:
            continue

        p = grid[(x, y)]
        is_visible = []
        for x2 in range(x + 1, end_x + 1):
            if grid[(x2, y)] >= p:
                is_visible.append(False)
                break
        for x3 in range(x - 1, -1, -1):
            if grid[(x3, y)] >= p:
                is_visible.append(False)
                break
        for y2 in range(y + 1, end_y + 1):
            if grid[(x, y2)] >= p:
                is_visible.append(False)
                break
        for y3 in range(y - 1, -1, -1):
            if grid[(x, y3)] >= p:
                is_visible.append(False)
                break

        if len(is_visible) < 4:
            visible_points.add((x, y))

    return len(visible_points) + edge_count


def prod(iterable):
    p = 1
    for n in iterable:
        p *= n
    return p


@timing()
def part2(lines: list[list[int]]) -> int:
    grid = create_grid(lines)
    score: dict[tuple[int, int], int] = {}
    end_x, end_y = max(grid)

    for x, y in grid:
        if x == 0 or y == 0 or x == end_x or y == end_y:
            continue

        p = grid[(x, y)]
        is_visible = [0, 0, 0, 0]
        # right
        for x2 in range(x + 1, end_x + 1):
            is_visible[2] = x2 - x
            if grid[(x2, y)] >= p:
                break
        # left
        for x3 in range(x - 1, -1, -1):
            is_visible[1] = x - x3
            if grid[(x3, y)] >= p:
                break
        # down
        for y2 in range(y + 1, end_y + 1):
            is_visible[3] = y2 - y
            if grid[(x, y2)] >= p:
                break
        # up
        for y3 in range(y - 1, -1, -1):
            is_visible[0] = y - y3
            if grid[(x, y3)] >= p:
                break

        score[(x, y)] = prod(is_visible)

    return max(score.values())


def main() -> int:
    sample = read_file_int(__file__, "../../input/2022/08/sample.input")
    puzzle = read_file_int(__file__, "../../input/2022/08/puzzle.input")

    check_result(21, part1(sample))
    check_result(1717, part1(puzzle))

    check_result(8, part2(sample))
    check_result(321975, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
