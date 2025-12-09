import math
import sys
from typing import Callable, NamedTuple

from support import InputReader, asserter, timing

# https://en.wikipedia.org/wiki/Disjoint-set_data_structure


@asserter
def part1(input: list[str], n: int) -> int:
    return solve(input, lambda distances: distances[:n])


@asserter
def part2(input: list[str]) -> int:
    return solve(input, lambda distances: distances)


type Distances = list[tuple[int, ...]]


def solve(input: list[str], cb: Callable[[Distances], Distances]) -> int:
    boxes = [Point3d.parse(x) for x in input]

    distances: Distances = []
    for i, a in enumerate(boxes):
        for j, b in enumerate(boxes[i + 1:], i + 1):
            distances.append((a.dist(b), i, j))
    distances.sort(key=lambda x: x[0])

    circuits = list(range(len(boxes)))
    for _, a, b in cb(distances):
        if circuits[a] == circuits[b]:
            continue
        if merge(circuits, a, b):
            # part2
            return boxes[a].x * boxes[b].x

    # part1
    counts = [0] * len(circuits)
    for c in circuits:
        counts[c] += 1

    return math.prod(sorted(counts)[-3:])


def merge(circ: list[int], a: int, b: int) -> bool:
    a = circ[a]
    b = circ[b]

    connect = True
    for i, c in enumerate(circ):
        if c == b:
            circ[i] = a
            continue
        connect &= c == a

    return connect


class Point3d(NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def parse(cls, s: str) -> Point3d:
        return cls(*map(int, s.split(",")))

    def dist(self, other: Point3d) -> int:
        a = (self.x - other.x) ** 2
        b = (self.y - other.y) ** 2
        c = (self.z - other.z) ** 2
        return math.isqrt(a + b + c)

    def __repr__(self) -> str:
        return f"({self.x} {self.y} {self.z})"


@timing("day8")
def main() -> int:
    i = InputReader(2025, 8).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, 10)(40)
        assert part1(puzzle, 1000)(131580)

    def s2() -> None:
        assert part2(example)(25272)
        assert part2(puzzle)(6844224)

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
