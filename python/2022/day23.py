import collections

from support import (
    Directions,
    Point,
    adjacents,
    assert_result,
    parse_coords_hash,
    read_file_raw,
    timing,
)

# DIRS = deque([
#     (-1 - 1j, -1j, 1 - 1j),
#     (-1 + 1j, 1j, 1 + 1j),
#     (-1 - 1j, -1, -1 + 1j),
#     (1 - 1j, 1, 1 + 1j),
# ])
VALID_DIRECTIONS: list[tuple[tuple[int, int], ...]] = [
    # NOTE: flip N/S to match how input was parsed
    (Directions.S, Directions.SE, Directions.SW),
    (Directions.N, Directions.NE, Directions.NW),
    (Directions.W, Directions.NW, Directions.SW),
    (Directions.E, Directions.NE, Directions.SE),
]


def move(
    limit: int,
    coords: set[Point],
) -> tuple[set[Point], int]:
    valid_moves = list(VALID_DIRECTIONS)
    round = 0
    while True:
        if round == limit:
            break

        round += 1

        moves: dict[Point, list[Point]]
        moves = collections.defaultdict(list)

        for x, y in coords:
            if all(
                (cx, cy) not in coords for cx, cy in adjacents(x, y, diagonals=True)
            ):
                continue

            for lookahead_points in valid_moves:
                move_dir = Point(*lookahead_points[0])
                if all((x + dx, y + dy) not in coords for dx, dy in lookahead_points):
                    moves[move_dir.move_by(x, y)].append(Point(x, y))
                    break

        moved = {k: v[0] for k, v in moves.items() if len(v) == 1}
        coords = (coords - set(moved.values())) | moved.keys()

        # rotate
        valid_moves = valid_moves[1:] + valid_moves[:1]

        if not moved:
            break

    return coords, round


@timing("part1")
def part1(input: str) -> int:
    coords, _ = move(10, parse_coords_hash(input))
    bx, by = [(min(b), max(b)) for b in zip(*coords)]
    return (bx[1] - bx[0] + 1) * (by[1] - by[0] + 1) - len(coords)


@timing("part2")
def part2(input: str) -> int:
    _, rounds = move(9999, parse_coords_hash(input))
    return rounds


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/23/sample")
    puzzle = read_file_raw(__file__, "../../input/2022/23/puzzle")

    assert_result(110, part1(sample))
    assert_result(3996, part1(puzzle))

    assert_result(20, part2(sample))
    assert_result(908, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
