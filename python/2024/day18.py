import heapq
import sys

from support import InputReader, asserter, timing

P = tuple[int, int]
DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Memory:
    grid: list[tuple[int, int]]

    def __init__(
        self, locations: list[tuple[int, int]], max_x: int, max_y: int
    ) -> None:
        self.locations = locations
        self.max_x = max_x
        self.max_y = max_y
        self.grid = []

    @classmethod
    def parse(cls, input: list[str], max_x: int, max_y: int) -> "Memory":
        positions = []
        for line in input:
            x, y = line.split(",")
            positions.append((int(x), int(y)))
        return cls(positions, max_x, max_y)

    def fill_memory_space(self, size: int) -> None:
        self.grid = []
        a = self.locations[:size]
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if (x, y) not in a:
                    self.grid.append((x, y))

    def find_shortest(self) -> int:
        start = (0, 0)
        end = (self.max_x, self.max_y)

        todo: list[tuple[int, P, int]]
        todo = [(0, end, 0)]

        visited = set()

        while todo:
            score, p, dir = heapq.heappop(todo)

            if p == start:
                return score

            if (p, dir) in visited:
                continue
            visited.add((p, dir))

            for i, d in enumerate(DIRS):
                (dx, dy) = d
                n = p[0] + dx, p[1] + dy

                if n in self.grid:
                    heapq.heappush(todo, (score + 1, n, i))

        raise AssertionError("unreachable")


@asserter
def part1(mem: Memory, size: int) -> int:
    mem.fill_memory_space(size)
    return mem.find_shortest()


@asserter
def part2(mem: Memory, min_size: int) -> str:
    for size in range(len(mem.locations), min_size, -1):
        try:
            mem.fill_memory_space(size)
            mem.find_shortest()
            (x, y) = mem.locations[size]
            return f"{x},{y}"
        except AssertionError:
            pass
    raise AssertionError("unreachable")


@timing("day18")
def main() -> int:
    i = InputReader(2024, 18).lines

    example = Memory.parse(i("example"), 6, 6)
    puzzle = Memory.parse(i("puzzle"), 70, 70)

    def s1() -> None:
        assert part1(example, 12)(22)
        assert part1(puzzle, 1024)(292)

    def s2() -> None:
        assert part2(example, 12)("6,1")
        assert part2(puzzle, 1024)("58,44")

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
