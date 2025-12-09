from __future__ import annotations

import sys
from typing import NamedTuple

from support import InputReader, asserter, timing


@asserter
def part1(input: list[str]) -> int:
    coords = [Point2d.parse(x) for x in input]
    size = len(coords)
    best = 0
    for i in range(size - 1):
        for j in range(i + 1, size):
            best = max(best, coords[i].area(coords[j]))
    return best


@asserter
def part2(input: list[str]) -> int:
    coords = [Point2d.parse(x) for x in input]

    # _print(coords)

    edges = [Rect.n(coords[i], coords[i + 1]) for i in range(len(coords) - 1)]
    edges.append(Rect.n(coords[-1], coords[0]))

    size = len(coords)
    best = 0
    for i in range(size - 1):
        for j in range(i + 1, size):
            rect = Rect.n(coords[i], coords[j])
            for e in edges:
                if e.intersects(rect):
                    break
            else:
                best = max(best, rect.area())

    return best


def _print(coords: list[Point2d]):
    lookup_x: dict[int, int] = {}
    lookup_y = lookup_x.copy()

    def get(i: int):
        p = coords[i]
        return lookup_x[p.x], lookup_y[p.y]

    for i, x in enumerate(sorted(set(p.x for p in coords))):
        lookup_x[x] = i  # * 2

    for i, y in enumerate(sorted(set(p.y for p in coords))):
        lookup_y[y] = i  # * 2

    size = len(coords)
    outline: set[tuple[int, int]] = set()

    max_x = 0
    max_y = 0

    for i in range(size):
        x1, y1 = get(i)
        x2, y2 = get((i + 1) % size)

        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                outline.add((x1, y))
        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                outline.add((x, y1))

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in outline:
                print("x", end="")
            else:
                print(" ", end="")
        print()


class Rect(NamedTuple):
    a: Point2d  # top-left
    b: Point2d  # bottom-right

    @classmethod
    def n(cls, a: Point2d, b: Point2d) -> Rect:
        return cls(
            Point2d(min(a.x, b.x), min(a.y, b.y)),
            Point2d(max(a.x, b.x), max(a.y, b.y)),
        )

    def intersects(self, other: Rect) -> bool:
        return (
            self.a.x < other.b.x
            and self.b.x > other.a.x
            and self.a.y < other.b.y
            and self.b.y > other.a.y
        )

    def area(self) -> int:
        return self.b.area(self.a)


class Point2d(NamedTuple):
    x: int
    y: int

    @classmethod
    def parse(cls, s: str) -> Point2d:
        return cls(*map(int, s.split(",")))

    def area(self, other: Point2d) -> int:
        a = abs(self.x - other.x) + 1
        b = abs(self.y - other.y) + 1
        return a * b

    def __repr__(self) -> str:
        return f"({self.x} {self.y})"


@timing("day9")
def main() -> int:
    i = InputReader(2025, 9).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(50)
        assert part1(puzzle)(4735268538)

    def s2() -> None:
        assert part2(example)(24)
        assert part2(puzzle)(1537458069)

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
