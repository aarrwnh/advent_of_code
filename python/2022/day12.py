import curses  # type: ignore
import heapq
from typing import Callable, Generator, NewType

from support import assert_result  # type: ignore
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
            if next_coord in grid and next_coord not in path:
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


def draw(stdscr, grid, paths) -> int:
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, 69, 232)
    curses.init_pair(2, 255, -1)

    #  if curses.can_change_color():
    #      curses.init_color(
    #          255, 0x1E * 1000 // 0xFF, 0x77 * 1000 // 0xFF, 0xD3 * 1000 // 0xFF
    #      )
    #      curses.init_pair(3, 255, -1)

    while True:

        for path in paths:
            stdscr.clear()
            for y, row in enumerate(grid):
                for x, p in enumerate(row):
                    stdscr.addstr(
                        y,
                        x,
                        p if (x, y) in path else " ",
                        curses.color_pair(1) if (x, y) in path else curses.COLOR_WHITE,
                    )

            stdscr.refresh()
            curses.delay_output(1)

        char = stdscr.get_wch()
        if char:
            break

    return 0


@timing()
def part1(input: str) -> int:
    lines = input.strip().splitlines()
    grid, start, end = create_grid(lines)

    def check(n: int, p: int) -> bool:
        return -5 <= n - p <= 1

    visited = []
    for length, pos, path in search(grid, start, check):
        visited.append(path)
        if pos == end:
            #  curses.wrapper(draw, lines, visited)
            print_grid_path(lines, path)  # type: ignore
            return length

    raise AssertionError("!")


@timing()
def part2(input: str) -> int:
    lines = input.strip().splitlines()
    grid, _, end = create_grid(lines)

    def check(n: int, p: int) -> bool:
        return 5 >= n - p >= -1

    visited = []
    for length, pos, path in search(grid, end, check):
        visited.append(path)
        if grid[pos] == ord("a"):
            #  curses.wrapper(draw, lines, visited)
            print_grid_path(lines, path)  # type: ignore
            return length

    raise AssertionError("!")


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/12/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/12/puzzle.input")

    assert_result(31, part1(sample))
    assert_result(339, part1(puzzle))

    assert_result(29, part2(sample))
    assert_result(332, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
