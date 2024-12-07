import sys
from collections import deque

from support import InputReader, Point, asserter, timing


class Stepper:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __init__(self, g: tuple[dict[Point, str], int, int, Point]) -> None:
        grid, width, height, start = g
        self.blocks = {p: ch for p, ch in grid.items() if ch == "#"}
        assert width == height
        self.size = width
        self.start = start

    def move(self, visited: set[Point]) -> set[Point]:
        nvisited = set()
        for p in visited:
            for dx, dy in self.directions:
                np = p.apply(Point(dx, dy))
                wp = Point((np.x % self.size), (np.y % self.size))
                # if wp in self.grid and self.grid[wp] != "#":
                if wp not in self.blocks:
                    nvisited.add(np)
        return nvisited


@asserter
@timing("part1")
def part1(g: Stepper, max_steps: int = 1) -> int:
    visited = set((g.start,))
    for _ in range(max_steps):
        visited = g.move(visited)
    return len(visited)


@asserter
@timing("part2")
def part2(g: Stepper, max_steps: int = 1) -> int:
    samples: deque[int] = deque([0] * 4, maxlen=4)
    visited = set((g.start,))
    from_center = max_steps % g.size
    for i in range(max_steps):
        if i % 100 == 99:
            print(f"  ({max_steps}) step={i} \tvisited={len(visited)}")

        if i == max_steps:
            return len(visited)

        if i % g.size == from_center:
            samples.append(len(visited))
            x1, x2, x3, x4 = samples
            if x4 - 3 * x3 + 3 * x2 - x1 == 0:
                assert (max_steps - i) % g.size == 0
                delta = (max_steps - i) / g.size
                # a + b + c
                # 3a + b
                # 2a
                a = x2 - 2 * x3 + x4
                b = x2 - 4 * x3 + 3 * x4
                c = 2 * x4
                return int(((a * delta + b) * delta + c) / 2)

        visited = g.move(visited)

        # 26501365 = 65 + (202300 * 131)
        #            ^ steps from center to edge

        # if i % 131 == 0:
        #     delta = len(visited) - count
        #     count = len(visited)
        #     print(len(visited), delta, delta - prev_count)
        #     prev_count = delta
        #
        #  15861  15857 15853
        #  62512  46651 30794
        # 139957  77445 30794
        # 248196 108239 30794
        # 387229 139033 30794

        # f(n) = a*n^2 + b*n + c

        # for y in range(height):
        #     for x in range(width):
        #         p = Point(x, y)
        #         if p in visited:
        #             print("O", end="")
        #         else:
        #             print(grid[p], end="")
        #     print()

    return len(visited)


def main() -> int:
    i = InputReader(2023, 21).grid2

    sample = Stepper(i("sample", find_start="S"))
    puzzle = Stepper(i("puzzle", find_start="S"))

    def s1() -> None:
        assert part1(sample, 6)(16)
        assert part1(puzzle, 64)(3795)

    def s2() -> None:
        assert part2(sample, 6)(16)
        assert part2(sample, 10)(50)
        assert part2(sample, 50)(1594)
        assert part2(sample, 100)(6536)
        assert part2(sample, 500)(167004)
        assert part2(sample, 1000)(668697)
        assert part2(sample, 5000)(16733044)  # 155 ms

    def s3() -> None:
        assert part2(puzzle, 26501365)(630129824772393)  # 57926 ms

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case [_, "3"]:
            s3()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
