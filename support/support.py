from __future__ import annotations

import contextlib
import os.path
import sys
import time
from typing import Any, Callable, Generator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def dist_to(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)

    @classmethod
    def parse(cls, s: str):
        x, y = s.split(",")
        return cls(int(x), int(y))


@contextlib.contextmanager
def timing(name: str = "") -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = "ms"
        if t < 100:
            t *= 1000
            unit = "μs"
        if name:
            name = f" ({name})"
        print(f"> {int(t)} {unit}{name}", file=sys.stderr, flush=True)


def red(s: str):
    print(f"  \x1b[41m\x1b[30m {s} \x1b[0m")


def green(s: str):
    print(f"  \x1b[48;5;28m\x1b[97m {s} \x1b[0m")


def check_result(expected: Any, result: Any) -> None:
    output = f"{result} == {expected}"
    if result == expected:
        green(output)
    else:
        red(output)


def read_file_raw(__file__: str, filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return f.read()


def read_file_lines(__file__: str, filename: str) -> list[str]:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def read_file(__file__: str, filename: str) -> list[str]:
    """
    @deprecated
    """
    return read_file_lines(__file__, filename)


def read_file_split(__file__: str, filename: str) -> list[list[str]]:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return [line.strip().split() for line in f.readlines()]


def read_file_int(__file__: str, filename: str) -> list[list[int]]:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return [[int(x) for x in line.strip()] for line in f.readlines()]


def read_file_int2(__file__: str, filename: str) -> list[int]:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "r") as f:
        return [int(line) for line in f.readlines()]


#  def adjacents(x: int, y: int) -> Generator[tuple[int, int], None, None]:
#      yield x, y + 1
#      yield x + 1, y
#      yield x - 1, y
#      yield x, y - 1


def in_bounds(arr: list[list[int]], y: int, x: int) -> bool:
    height = len(arr)
    width = len(arr[0])
    return x >= 0 and x < width and y >= 0 and y < height


def adjacents(
    x: int,
    y: int,
    diagonals: bool = False,
) -> Generator[tuple[int, int], None, None]:
    coords = (-1, 0, 1)
    for x_d in coords:
        for y_d in coords:
            if x_d == y_d == 0:
                continue
            if diagonals is False and abs(x_d) == abs(y_d):
                continue
            yield x + x_d, y + y_d


def adjacents_bounds(
    arr: list[list[int]],
    x: int,
    y: int,
    diagonals: bool = False,
) -> Generator[tuple[int, int], None, None]:
    coords = (-1, 0, 1)
    for x_d in coords:
        for y_d in coords:
            if x_d == y_d == 0:
                continue
            if diagonals is False and abs(x_d) == abs(y_d):
                continue
            if not in_bounds(arr, x + x_d, y + y_d):
                continue
            yield x + x_d, y + y_d


def make_point_range(start: int, stop: int):
    is_reverse = -1 if start > stop else 1
    return [*range(start, stop + is_reverse, is_reverse)]
    #  return [*range(min(start, stop), max(start, stop) + 1)]


def fill_points(x1: int, y1: int, x2: int, y2: int, diagonals: bool = False):
    x_points = make_point_range(x1, y1)
    y_points = make_point_range(x2, y2)
    len_x = len(x_points)
    len_y = len(y_points)

    if diagonals:
        pass
        #  if len_x > len_y:
        #      y_points = [y1] * len_x
        #  elif len_x < len_y:
        #      x_points = [x1] * len_y
    else:
        if x1 == y1:
            x_points = [x1] * len_y
        elif x2 == y2:
            y_points = [x2] * len_x
        else:
            return []

    if len(x_points) != len(y_points):
        raise AssertionError("x and y are not equal")

    return zip(x_points, y_points)


def format_coords_hash(
    coords: set[tuple[int, int]] | set[Point],
    *,
    flip_y=False,
    flip_x=False,
    cb: Callable[[int, int], str] | None = None,
) -> str:
    y: list[int] = []
    x: list[int] = []
    for xx, yy in coords:
        x.append(xx)
        y.append(yy)

    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)

    range_x = range(max_x, min_x - 1, -1) if flip_x else range(min_x, max_x + 1)
    range_y = range(max_y, min_y - 1, -1) if flip_y else range(min_y, max_y + 1)

    return "\n".join(
        "".join(cb(x, y) if cb else "#" if (x, y) in coords else " " for x in range_x)
        for y in range_y
    )


def create_number_grid(lines: list[list[int]]) -> dict[tuple[int, int], int]:
    grid: dict[tuple[int, int], int] = {}

    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            grid[(x, y)] = int(p)

    return grid


def create_grid(lines: list[list[str]]) -> dict[tuple[int, int], str]:
    grid: dict[tuple[int, int], str] = {}

    for y, row in enumerate(lines):
        for x, p in enumerate(row):
            grid[(x, y)] = p

    return grid
