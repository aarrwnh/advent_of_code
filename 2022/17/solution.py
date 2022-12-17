import itertools

from support import format_coords_hash  # type: ignore
from support import check_result, read_file_raw, timing

MAGIC = 69
WIDTH = 7
"""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


SHAPES: list[list[list[int]]] = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]


def shape_to_coords(x: int, y: int, current: list[list[int]]):
    coords: set[tuple[int, ...]] = set()
    #  print(pos, current)
    for i in range(len(current)):
        row = current[i]
        for j, v in enumerate(row):
            if v == 1:
                p = (x + j, y + i)
                coords.add(p)
    return coords


def move(
    x: int,
    y: int,
    shape: list[list[int]],
    movement: tuple[int, int],
    coords: set[tuple[int, int]],
):
    for i, row in enumerate(shape):
        for j, v in enumerate(row):
            if v == 1:
                p = (x + j + movement[0], y + i + movement[1])
                if p in coords:
                    return x, y
    return [x + movement[0], y + movement[1]]


@timing("part1")
def part1_first(input: str) -> int:
    max_height = 0
    directions = itertools.cycle(input)
    occupied = {(x, 0) for x in range(0, 8)}

    for i in range(2022):
        current = SHAPES[i % 5]
        pos = [3, max_height + 4]

        while True:
            # push left/right
            direction = next(directions)
            if direction == "<" and pos[0] > 1:
                pos = move(pos[0], pos[1], current, (-1, 0), occupied)
            elif direction == ">" and pos[0] + len(current[0]) <= WIDTH:
                pos = move(pos[0], pos[1], current, (1, 0), occupied)

            next_pos = move(pos[0], pos[1], current, (0, -1), occupied)

            if next_pos == pos:
                occupied |= shape_to_coords(pos[0], pos[1], current)
                max_height = max(y for _, y in occupied)
                # trim far and unreachable points
                obsolete = set(p for p in occupied if p[1] + MAGIC < max_height)
                occupied -= obsolete
                break
            else:
                pos = next_pos

    return max_height


def get_fingerprint(
    piece_id: int,
    gas_id: int,
    coords: set[tuple[int, int]],
) -> tuple[int, int, frozenset[tuple[int, int]]]:
    max_ys = []
    for i in range(0, WIDTH):
        a = [y for x, y in coords if x == i]
        if len(a) > 0:
            max_ys.append(max(a))
    min_y = min(max_ys)
    return (
        piece_id,
        gas_id,
        frozenset((x, y - min_y) for x, y in coords if y >= min_y),
    )


def compute(input: str, tower_height: int = 1_000_000_000_000) -> int:
    occupied = {(x, 0) for x in range(0, 7)}

    directions = itertools.cycle(enumerate(input))
    max_height = 0

    fingerprints: dict[
        tuple[int, int, frozenset[tuple[int, int]]], tuple[int, int]
    ] = {}

    done_at = None
    done_at_val = None
    done_at_delta_height = None

    direction_id = 0

    for i in range(tower_height + 1):
        current = SHAPES[i % 5]
        x = 2
        y = max_height + 4

        key = get_fingerprint(i % 5, direction_id, occupied)

        if key in fingerprints:
            # math pain by @anthonywritescode
            start_i, start_height = fingerprints[key]
            period = i - start_i
            remaining = tower_height - start_i
            n = remaining // period
            done_at = i + (remaining % period)
            done_at_val = start_height + n * (max_height - start_height)
            done_at_delta_height = max_height
        else:
            fingerprints[key] = (i, max_height)

        if done_at is not None and i == done_at:
            assert done_at_val is not None
            assert done_at_delta_height is not None
            return done_at_val + (max_height - done_at_delta_height)

        while True:
            direction_id, direction = next(directions)

            if direction == "<" and x > 0:
                (x, _) = move(x, y, current, (-1, 0), occupied)
            elif direction == ">" and x + len(current[0]) < WIDTH:
                (x, _) = move(x, y, current, (1, 0), occupied)

            (_, next_y) = move(x, y, current, (0, -1), occupied)
            if next_y == y:
                occupied |= shape_to_coords(x, y, current)
                max_height = max(y for _, y in occupied)
                # trim far and unreachable points
                obsolete = set(p for p in occupied if p[1] + MAGIC < max_height)
                occupied -= obsolete
                break
            else:
                y = next_y

    raise AssertionError(f"{max_height}")


@timing("part1")
def part1(input: str) -> int:
    return compute(input, 2022)


@timing("part2")
def part2(input: str) -> int:
    return compute(input, 1_000_000_000_000)


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/17/sample.input").strip()
    puzzle = read_file_raw(__file__, "../../input/2022/17/puzzle.input").strip()

    check_result(3068, part1(sample))
    check_result(3227, part1(puzzle))

    check_result(1514285714288, part2(sample))
    check_result(1597714285698, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
