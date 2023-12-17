import heapq
import sys

from support import InputReader, Point, asserter, timing

DIRS = [
    (1, 0),
    (0, 1),
    (0, -1),
    (-1, 0),
]


@asserter
@timing("part1")
def part1(g: tuple[dict[Point, str], int, int, Point]) -> int:
    (grid, width, height, start) = g
    end = Point(width - 1, height - 1)

    queue: list[tuple[int, int, tuple[int, int], Point, set[Point]]]
    queue = [(0, 0, (0, 0), start, {start})]
    seen: dict[tuple[Point, tuple[int, int], int], int] = {}

    while queue:
        heat_loss, step, dir, prev, path = heapq.heappop(queue)

        if prev == end:
            return heat_loss

        if heat_loss > seen.get((prev, dir, step), sys.maxsize):
            continue

        if step < 3 and dir != (0, 0):
            n = prev.apply(Point(*dir))
            if n in grid and n not in path:
                next_cost = heat_loss + int(grid[n])
                if next_cost < seen.get((n, dir, step + 1), sys.maxsize):
                    seen[(n, dir, step + 1)] = next_cost
                    heapq.heappush(
                        queue,
                        (
                            next_cost,
                            step + 1,
                            dir,
                            n,
                            path | {n},
                        ),
                    )

        for dx, dy in DIRS:
            if (dx, dy) != (dir[0], dir[1]) and (dx, dy) != (-dir[0], -dir[1]):
                n = prev.apply(Point(dx, dy))
                if n in grid and n not in path:
                    next_cost = heat_loss + int(grid[n])
                    if next_cost < seen.get((n, (dx, dy), 1), sys.maxsize):
                        seen[(n, (dx, dy), 1)] = next_cost
                        heapq.heappush(
                            queue,
                            (
                                next_cost,
                                1,
                                (dx, dy),
                                n,
                                path | {n},
                            ),
                        )

    raise AssertionError("unreachable")


@asserter
@timing("part2")
def part2(g: tuple[dict[Point, str], int, int, Point]) -> int:
    (grid, width, height, start) = g
    end = Point(width - 1, height - 1)

    queue: list[tuple[int, int, tuple[int, int], Point, set[Point]]]
    queue = [(0, 0, (0, 0), start, {start})]
    seen: dict[tuple[Point, tuple[int, int], int], int] = {}

    while queue:
        heat_loss, step, dir, prev, path = heapq.heappop(queue)

        if prev == end:
            return heat_loss

        if heat_loss > seen.get((prev, dir, step), sys.maxsize):
            continue

        if step < 10 and dir != (0, 0):
            n = prev.apply(Point(*dir))
            if n in grid and n not in path:
                next_cost = heat_loss + int(grid[n])
                if next_cost < seen.get((n, dir, step + 1), sys.maxsize):
                    seen[(n, dir, step + 1)] = next_cost
                    heapq.heappush(
                        queue,
                        (
                            next_cost,
                            step + 1,
                            dir,
                            n,
                            path | {n},
                        ),
                    )

        if step >= 4 or (dir[0], dir[1]) == (0, 0):
            for dx, dy in DIRS:
                if (dx, dy) != (dir[0], dir[1]) and (dx, dy) != (-dir[0], -dir[1]):
                    n = prev.apply(Point(dx, dy))
                    if n in grid and n not in path:
                        next_cost = heat_loss + int(grid[n])
                        if next_cost < seen.get((n, (dx, dy), 1), sys.maxsize):
                            seen[(n, (dx, dy), 1)] = next_cost
                            heapq.heappush(
                                queue,
                                (
                                    next_cost,
                                    1,
                                    (dx, dy),
                                    n,
                                    path | {n},
                                ),
                            )

    raise AssertionError("unreachable")


def main() -> int:
    i = InputReader(2023, 17).grid

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(102)
        assert part1(puzzle)(847)

    def s2() -> None:
        assert part2(sample)(94)
        assert part2(puzzle)(997)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
