import heapq

from support import adjacents, check_result, read_file_raw, timing  # type: ignore


def create_grid(
    lines: list[str],
) -> tuple[dict[tuple[int, int], int], tuple[int, int], tuple[int, int]]:
    grid: dict[tuple[int, int], int] = {}
    start = (0, 0)
    end = (0, 0)

    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            grid[(x, y)] = ord(p)
            if p == "S":
                start = (x, y)
            elif p == "E":
                end = (x, y)

    grid[start] = ord("a")
    grid[end] = ord("z")

    return grid, start, end


@timing()
def part1(input: str) -> int:
    grid, start, end = create_grid(input.strip().splitlines())
    queue: list[tuple[int, tuple[int, int], set[tuple[int, int]]]] = [
        (0, start, {start})
    ]

    best_path: set[tuple[int, int]] = set()
    best_at: dict[tuple[int, int], int] = {}
    best = 0

    while queue:
        length, last_coord, path = heapq.heappop(queue)

        if last_coord in best_at and length >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = length

        if last_coord == end:
            best = length
            best_path = path
            break

        for next_coord in adjacents(*last_coord):
            if next_coord in grid:
                if grid[next_coord] - grid[last_coord] <= 1:
                    heapq.heappush(
                        queue,
                        (
                            length + 1,
                            next_coord,
                            path | {next_coord},
                        ),
                    )

    #  print(len(best_path))
    #  print(format_coords_hash(best_path))

    return best


@timing()
def part2(input: str):
    grid, _, end = create_grid(input.strip().splitlines())
    queue: list[tuple[int, tuple[int, int]]] = [(0, end)]
    path: set[tuple[int, int]] = set()

    while queue:
        length, last_coord = heapq.heappop(queue)

        if grid[last_coord] == ord("a"):
            return length
        elif last_coord in path:
            continue
        else:
            path.add(last_coord)

        for next_coord in adjacents(*last_coord):
            if next_coord in grid:
                if grid[next_coord] - grid[last_coord] >= -1:
                    heapq.heappush(
                        queue,
                        (length + 1, next_coord),
                    )


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/12/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/12/puzzle.input")

    check_result(31, part1(sample))
    check_result(339, part1(puzzle))

    check_result(29, part2(sample))
    check_result(332, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
