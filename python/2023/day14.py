import enum
from collections.abc import Iterable

from support import InputReader, Point, asserter, timing


class Dirs(enum.Enum):
    North = (-1, 0)  # NORTH
    West = (0, -1)  # WEST
    South = (1, 0)  # SOUTH
    East = (0, 1)  # EAST


def _get_ranges(dir: Dirs, width: int, height: int) -> tuple[range, range, int, int]:
    down = range(0, height)
    up = range(height - 1, -1, -1)

    right = range(0, width)
    left = range(width - 1, -1, -1)

    match dir:
        case Dirs.North:
            return (down, right, -1, 0)
        case Dirs.West:
            return (left, down, 0, -1)
        case Dirs.South:
            return (up, left, 1, 0)
        case Dirs.East:
            return (down, left, 0, 1)

    raise AssertionError("unreachable")


def tilt(grid: dict[Point, str], dir: Dirs, width: int, height: int) -> None:
    rows, cols, dr, dc = _get_ranges(dir, width, height)

    for row in rows:
        for col in cols:
            ch = grid[Point(col, row)]
            if ch == "O":
                r = row
                c = col

                while (
                    r + dr >= 0
                    and c + dc >= 0
                    and r + dr < height
                    and c + dc < width
                    and grid[Point(c + dc, r + dr)] == "."
                ):
                    r += dr
                    c += dc

                if (c, r) != (col, row):
                    grid[Point(c, r)] = ch
                    grid[Point(col, row)] = "."


def total_load(height: int, grid: Iterable[Point]) -> int:
    total = 0
    for p in grid:
        total += height - p.y
    return total


@asserter
@timing("part1")
def part1(grid_data: tuple[dict[Point, str], int, int, int]) -> int:
    (grid, width, height, _) = grid_data

    grid = grid.copy()

    tilt(grid, Dirs.North, width, height)

    return total_load(
        height,
        (p for p in grid if grid[p] == "O"),
    )


@asserter
@timing("part2")
def part2(grid_data: tuple[dict[Point, str], int, int, int]) -> int:
    (grid, width, height, _) = grid_data

    grid = grid.copy()
    total_cycles = 1000000000
    fingerprints: dict[frozenset[Point], int] = {}

    for cycle in range(total_cycles):
        for d in Dirs:
            tilt(grid, d, width, height)

        key = frozenset(p for p in grid if grid[p] == "O")
        if key in fingerprints:
            start_i = fingerprints[key]
            period = cycle - start_i
            remaining = total_cycles - start_i
            phase = remaining % period
            done_at = start_i + phase - 1

            for idx, p in enumerate(fingerprints):
                if idx == done_at:
                    return total_load(height, p)
        else:
            fingerprints[key] = cycle

    raise AssertionError("unreachable")


def main() -> int:
    i = InputReader(2023, 14)

    sample = i.grid("sample")
    puzzle = i.grid("puzzle")

    part1(sample)(136)
    part1(puzzle)(108857)

    part2(sample)(64)
    part2(puzzle)(95273)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
