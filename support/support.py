import contextlib
import os.path
import sys
import time
from typing import Generator

HERE = os.path.dirname(os.path.abspath(__file__))


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


def check_result(expected: any, result: any) -> None:
    print(result == expected, f"{result} == {expected}")


def read_file(__file__: str, filename: str) -> list[str]:
    lines: list[str] = []
    path = os.path.dirname(__file__) + "/" + filename
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.rstrip().split()
            lines.append(line[0])
    return lines


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
