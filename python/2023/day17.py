import heapq
import sys
from typing import NamedTuple

from support import InputReader, Point, asserter, timing

DIRS = [(1, 0), (0, 1), (0, -1), (-1, 0)]


class State(NamedTuple):
    prev: Point
    dir: tuple[int, int]
    step: int


class Crucible:
    def __init__(self, g: tuple[dict[Point, str], int, int, Point]) -> None:
        (grid, width, height, start) = g
        self.grid = grid
        self.start = start
        self.end = Point(width - 1, height - 1)
        self.zero = (0, 0)

    def _new_state(
        self,
        p: Point,
        heat_loss: int,
        dir: tuple[int, int],
        step: int,
    ) -> tuple[int, State] | None:
        n = p.apply(Point(*dir))
        if n in self.grid:
            next_cost = heat_loss + int(self.grid[n])
            return (next_cost, State(n, dir, step))
        return None

    def _next_blocks(
        self,
        heat_loss: int,
        prev: State,
    ) -> list[tuple[int, State] | None]:
        cand = []
        (p, dir, step) = prev

        if step < self.max_step and dir != self.zero:
            cand.append(self._new_state(p, heat_loss, dir, step + 1))

        if step >= self.min_step or dir == self.zero:
            for dx, dy in DIRS:
                if (dx, dy) != dir and (dx, dy) != (-dir[0], -dir[1]):  # do not go back
                    cand.append(self._new_state(p, heat_loss, (dx, dy), 1))

        return cand

    def dijkstra(self, *, max_step: int, min_step: int = 0) -> int:
        queue: list[tuple[int, State]] = [(0, State(self.start, self.zero, 0))]
        seen: dict[State, int] = {}
        self.max_step = max_step
        self.min_step = min_step

        while queue:
            prev_cost, prev_state = heapq.heappop(queue)

            if prev_state[0] == self.end:
                return prev_cost

            if prev_cost > seen.get(prev_state, sys.maxsize):
                continue

            for n in self._next_blocks(prev_cost, prev_state):
                if not n:
                    continue
                next_cost, state = n
                if next_cost < seen.get(state, sys.maxsize):
                    seen[state] = next_cost
                    heapq.heappush(queue, (next_cost, state))

        raise AssertionError("unreachable")


@asserter
@timing("part1")
def part1(g: Crucible) -> int:
    return g.dijkstra(max_step=3)


@asserter
@timing("part2")
def part2(g: Crucible) -> int:
    return g.dijkstra(max_step=10, min_step=4)


def main() -> int:
    i = InputReader(2023, 17).grid

    sample = Crucible(i("sample"))
    puzzle = Crucible(i("puzzle"))

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
