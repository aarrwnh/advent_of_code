import heapq
from typing import Callable, Generator, NewType

from support import check_result  # type: ignore
from support import adjacents, read_file_raw, timing

Point = NewType("Point", tuple[int, int])


def create_grid(
    lines: list[str],
) -> tuple[dict[Point, int], Point, Point]:
    grid: dict[Point, int] = {}
    start: Point = Point((0, 0))
    end: Point = Point((0, 0))

    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            grid[Point((x, y))] = ord(p)
            if p == "S":
                start = Point((x, y))
            elif p == "E":
                end = Point((x, y))

    grid[start] = ord("a")
    grid[end] = ord("z")

    return grid, start, end


def search(
    grid: dict[Point, int], start: Point, fn: Callable[[int, int], bool]
) -> Generator[tuple[int, Point, set[Point]], None, None]:
    queue: list[tuple[int, Point, set[Point]]] = [(0, start, {start})]
    best_at: dict[Point, int] = {}

    while queue:
        length, last_coord, path = heapq.heappop(queue)

        yield length, last_coord, path

        if last_coord in best_at and length >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = length

        for next_coord in adjacents(*last_coord):
            if next_coord in grid:
                if fn(grid[next_coord], grid[last_coord]):
                    heapq.heappush(
                        queue,
                        (
                            length + 1,
                            next_coord,
                            path | {next_coord},
                        ),
                    )


def print_grid_path(grid: list[str], path: set[tuple[int, int]]) -> None:
    for y, row in enumerate(grid):
        new_row = []
        for x, p in enumerate(row):
            new_row.append(p if (x, y) in path else f"\x1b[38;5;239m{p}\x1b[0m")
        print("".join(new_row))


@timing()
def part1(input: str) -> int:
    lines = input.strip().splitlines()
    grid, start, end = create_grid(lines)

    def check(n: int, p: int) -> bool:
        return n - p <= 1

    for length, pos, path in search(grid, start, check):
        if pos == end:
            print_grid_path(lines, path)  # type: ignore
            return length

    raise AssertionError("!")


@timing()
def part2(input: str) -> int:
    lines = input.strip().splitlines()
    grid, _, end = create_grid(lines)

    def check(n: int, p: int) -> bool:
        return n - p >= -1

    for length, pos, path in search(grid, end, check):
        if grid[pos] == ord("a"):
            print_grid_path(lines, path)  # type: ignore
            return length

    raise AssertionError("!")


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
