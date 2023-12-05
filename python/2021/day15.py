import heapq

from support import timing, adjacents, check_result, read_file


def print_grid_path(
    grid: dict[tuple[int, int], int],
    path: set[tuple[int, int]],
    grid_size: int,
) -> None:
    for y in range(0, grid_size):
        print(
            "".join(
                [
                    f"{grid[(x,y)]}"
                    if (x, y) in path
                    else f"\x1b[38;5;239m{grid[(x,y)]}\x1b[0m"
                    for x in range(0, grid_size)
                ]
            )
        )


def create_grid(lines: list[str], multiply: int = 1) -> dict[tuple[int, int], int]:
    """assumes grid is 1:1 size"""
    original_size = len(lines)
    grid: dict[tuple[int, int], int] = {}

    for y, row in enumerate(lines):
        for x, point in enumerate(row):
            point = int(point)
            grid[(x, y)] = point

            for y_m in range(multiply):
                for x_m in range(multiply):
                    val = point + x_m + y_m
                    grid[(x_m * original_size + x, y_m * original_size + y)] = (
                        val % 9 if val >= 10 else val
                    )

    return grid


@timing()
def find_path(
    lines: list[str],
    grid_multiply: int = 1,
    print_path: bool = True,
) -> int:

    grid = create_grid(lines, grid_multiply)

    start = (0, 0)
    end = max(grid)

    #  queue = collections.deque([[frozenset([start]), start, 0]])
    queue: list[tuple[int, tuple[int, int], set[tuple[int, int]]]] = [
        (0, start, {start})
    ]

    best_path: set[tuple[int, int]] = set()
    best_at = {}
    best = None

    while len(queue) > 0:
        length, last_coord, path = heapq.heappop(queue)

        if last_coord in best_at and length >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = length

        if best and length >= best:
            continue
        elif last_coord == end:
            best = length
            best_path = path
            break

        for next_coord in adjacents(*last_coord):
            if next_coord in grid and next_coord not in path:
                heapq.heappush(
                    queue,
                    (
                        length + grid[next_coord],
                        next_coord,
                        path | {next_coord},
                    ),
                )

    if print_path:
        print_grid_path(grid, best_path, end[0] + 1)

    return best_at[end]


@timing("total")
def main() -> int:
    sample = read_file(__file__, "sample.input")
    puzzle = read_file(__file__, "puzzle.input")

    # part1
    check_result(40, find_path(sample, 1))
    check_result(811, find_path(puzzle, 1, False))

    # part2
    check_result(315, find_path(sample, 5))
    check_result(3012, find_path(puzzle, 5, False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
