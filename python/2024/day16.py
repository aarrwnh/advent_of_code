import heapq
import sys

from support import InputReader, asserter, timing

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
P = tuple[int, int]


def parse(lines: list[str]) -> tuple[P, P, list[P]]:
    start = None
    end = None
    grid: list[P] = []
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == "S":
                start = (x, y)
            elif ch == "E":
                end = (x, y)
            elif ch == ".":
                grid.append((x, y))
    assert start is not None
    assert end is not None
    grid.extend([start, end])
    return start, end, grid


def maybe_dijkstra(grid: list[P], start: P, end: P) -> int:
    todo: list[tuple[int, P, P]]
    todo = [(0, start, (1, 0))]

    visited = set()

    while todo:
        score, p, dir = heapq.heappop(todo)

        (dx, dy) = dir
        for d, s in [((dx, dy), 1), ((dy, -dx), 1001), ((-dy, dx), 1001)]:
            n = p[0] + d[0], p[1] + d[1]
            s += score

            if n == end:
                return s

            if n in grid and (n, d) not in visited:
                visited.add((n, d))
                heapq.heappush(todo, (s, n, d))

    raise AssertionError("unreachable")


@asserter
def part1(lines: list[str]) -> int:
    start, end, grid = parse(lines)
    return maybe_dijkstra(grid, start, end)


@asserter
def part2(lines: list[str]) -> int:
    start, end, grid = parse(lines)

    best_score = maybe_dijkstra(grid, start, end)

    best: dict[P, int] = {}
    todo: list[tuple[int, P, P, frozenset[P]]]
    todo = [(0, start, (1, 0), frozenset())]

    visited = set()
    places: set[P] = set((end,))

    while todo:
        score, p, dir, seen = heapq.heappop(todo)
        best_at = best.get(p, sys.maxsize)
        if score > best_at + 1000 or score > best_score:
            continue

        best[p] = min(score, best_at)

        if p == end and score == best_score:
            places.update(seen)
            continue

        visited.add((p, dir))

        (dx, dy) = dir
        for d, s in [((dx, dy), 1), ((dy, -dx), 1001), ((-dy, dx), 1001)]:
            n = p[0] + d[0], p[1] + d[1]

            if n in grid and (n, d) not in visited and n not in seen:
                heapq.heappush(todo, (score + s, n, d, seen | {p}))

    return len(places)


@timing("day16")
def main() -> int:
    i = InputReader(2024, 16).lines

    example1 = i("example-1")
    example2 = i("example-2")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example1)(7036)
        assert part1(example2)(11048)
        assert part1(puzzle)(98416)

    def s2() -> None:
        assert part2(example1)(45)
        assert part2(example2)(64)
        # assert part2(puzzle)(471)

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
