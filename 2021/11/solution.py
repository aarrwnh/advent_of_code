from typing import Generator, List, Tuple
import os
from support import timing


def read_file(filename: str) -> List[str]:
    lines: List[str] = []
    path = os.path.dirname(__file__) + "/" + filename
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            lines.append(line)
    return lines


def in_bounds(
    arr: List[List[int]],
    y: int,
    x: int,
):
    height = len(arr)
    width = len(arr[0])
    return x >= 0 and x < width and y >= 0 and y < height


def adjacents(
    arr: List[List[int]],
    x: int,
    y: int,
) -> Generator[Tuple[int, int], None, None]:
    for x_d in (-1, 0, 1):
        for y_d in (-1, 0, 1):
            if x_d == y_d == 0:
                continue
            if not in_bounds(arr, x + x_d, y + y_d):
                continue
            yield x + x_d, y + y_d


def chain_adjacent(
    arr: List[List[int]],
    x: int,
    y: int,
    seen_flash: List[Tuple[int, int]],
):
    for current_pos in adjacents(arr, x, y):
        x_d, y_d = current_pos
        arr[y_d][x_d] += 1
        if arr[y_d][x_d] > 9 and current_pos not in seen_flash:
            seen_flash.append(current_pos)
            chain_adjacent(arr, x_d, y_d, seen_flash)


@timing()
def compute(
    lines: List[str],
    step_count: int = 100,
    part2: bool = False,
) -> int:
    arr: List[List[int]] = [[int(c) for c in line] for line in lines]

    flash_count = 0
    for step in range(step_count):
        seen_flash: List[Tuple[int, int]] = []
        for y in range(len(arr)):
            for x in range(len(arr[y])):
                arr[y][x] += 1
                if arr[y][x] > 9 and (x, y) not in seen_flash:
                    seen_flash.append((x, y))
                    chain_adjacent(arr, x, y, seen_flash)

        for x, y in seen_flash:
            arr[y][x] = 0

        flash_count += len(seen_flash)

        if part2 and len(seen_flash) == 100:
            return step + 1

        #  print("---", step + 1)
        #  for line in arr:
        #      print("".join([str("\033[1m0\033[m" if c == 0 else c) for c in line]))
    return flash_count


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    example = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    check_result(1656, compute(example))
    check_result(1725, compute(puzzle))

    check_result(195, compute(example, 200, True))
    check_result(308, compute(puzzle, 309, True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
