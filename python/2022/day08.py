from support import create_number_grid  # type: ignore
from support import assert_result, read_file_int, timing


@timing()
def part1(lines: list[list[int]]) -> int:
    grid = create_number_grid(lines)

    end_x, end_y = max(grid)
    visible_trees = set()

    def c(x, y, start, stop, swap_coords):
        is_reverse = -1 if start > stop else 1
        tree_height = grid[(x, y)]
        visible_trees.add((x, y))
        for j in range(start, stop, is_reverse):
            next_tree = (j, y) if swap_coords else (x, j)
            if grid[next_tree] > tree_height:
                visible_trees.add(next_tree)
                tree_height = grid[next_tree]

    for x in range(0, end_x + 1):
        c(x, 0, 1, end_y + 1, False)  # right
        c(x, end_y, end_y, -1, False)  # left

    for y in range(0, end_y + 1):
        c(0, y, 1, end_x + 1, True)  # down
        c(end_x, y, end_x, -1, True)  # up

    return len(visible_trees)


def prod(iterable: list[int]) -> int:
    p = 1
    for n in iterable:
        p *= n
    return p


@timing()
def part2(lines: list[list[int]]) -> int:
    grid = create_number_grid(lines)
    score = 0
    end_x, end_y = max(grid)

    for x, y in grid:
        if x == 0 or y == 0 or x == end_x or y == end_y:
            continue

        tree_height = grid[(x, y)]
        if tree_height == 9:
            continue

        scenic_score = [0, 0, 0, 0]
        # right
        for x2 in range(x + 1, end_x + 1):
            scenic_score[2] = x2 - x
            if grid[(x2, y)] >= tree_height:
                break

        # left
        for x3 in range(x - 1, -1, -1):
            scenic_score[1] = x - x3
            if grid[(x3, y)] >= tree_height:
                break

        if scenic_score[2] * scenic_score[1] < 4:
            continue

        # down
        for y2 in range(y + 1, end_y + 1):
            scenic_score[3] = y2 - y
            if grid[(x, y2)] >= tree_height:
                break

        # up
        for y3 in range(y - 1, -1, -1):
            scenic_score[0] = y - y3
            if grid[(x, y3)] >= tree_height:
                break

        score = max(prod(scenic_score), score)

    return score


def main() -> int:
    sample = read_file_int(__file__, "../../input/2022/08/sample.input")
    puzzle = read_file_int(__file__, "../../input/2022/08/puzzle.input")

    assert_result(21, part1(sample))
    assert_result(1717, part1(puzzle))

    assert_result(8, part2(sample))
    assert_result(321975, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
