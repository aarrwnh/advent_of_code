import heapq
import sys

from support import InputReader, asserter, timing

P = tuple[int, int]
DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Memory:
    def __init__(self, input: list[str], size: int) -> None:
        self.max_x = size
        self.max_y = size
        self.corruptions: list[P] = []
        for line in input:
            x, y = line.split(",")
            self.corruptions.append((int(x), int(y)))

    def fill_memory_space(self, offset: int) -> None:
        self.bad_grid: set[P] = set(self.corruptions[0:offset])

    def find_shortest(self) -> None | int:
        start = (0, 0)
        end = (self.max_x, self.max_y)

        todo: list[tuple[int, P]]
        todo = [(0, end)]

        visited = set()

        while todo:
            cost, (x, y) = heapq.heappop(todo)

            for dx, dy in DIRS:
                n = x + dx, y + dy

                if n == start:
                    return cost + 1

                if (
                    n not in visited
                    and 0 <= x <= self.max_x
                    and 0 <= y <= self.max_y
                    and n not in self.bad_grid
                ):
                    heapq.heappush(todo, (cost + 1, n))
                    visited.add(n)

        return None


@asserter
def part1(mem: Memory, offset: int) -> int:
    mem.fill_memory_space(offset)
    steps = mem.find_shortest()
    assert steps is not None
    return steps


@asserter
def part2(mem: Memory, min_offset: int) -> str:
    min = min_offset
    max = len(mem.corruptions)

    while max > min:
        mid = (max + min) // 2
        mem.fill_memory_space(mid)
        if mem.find_shortest() is None:
            max = mid
        else:
            min = mid + 1

    (x, y) = mem.corruptions[max - 1]
    return f"{x},{y}"


@timing("day18")
def main() -> int:
    i = InputReader(2024, 18).lines

    example = Memory(i("example"), 6)
    puzzle = Memory(i("puzzle"), 70)

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
