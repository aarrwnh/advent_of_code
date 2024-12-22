import collections
import heapq
import sys

from support import InputReader, asserter, timing

P = tuple[int, int]

DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


class Racetrack:
    def __init__(self, input: str, min_cheat_time: int) -> None:
        self.min_cheat_time = min_cheat_time
        start_pos = None
        end_pos = None
        self.track: list[P] = []
        for y, row in enumerate(input.split("\n")):
            for x, p in enumerate(row.strip()):
                if p == "S":
                    start_pos = (x, y)
                elif p == "E":
                    end_pos = (x, y)
                if p != "#":
                    self.track.append((x, y))
        assert start_pos is not None
        assert end_pos is not None
        self.start = start_pos
        self.end = end_pos

        self._shortest_path()

    def _shortest_path(self) -> None:
        best: dict[P, int] = {}
        backtrack: dict[P, P] = {}

        visited = set()
        todo = [(0, self.start)]
        while todo:
            timecost, p = heapq.heappop(todo)
            if p == self.end:
                break
            visited.add(p)
            (x, y) = p
            for dx, dy in DIRS:
                n = x + dx, y + dy
                tc = timecost + 1
                if n not in self.track:
                    continue
                if n not in visited:
                    prev_cost = best.get(n, sys.maxsize)
                    if tc < prev_cost:
                        best[n] = tc
                        backtrack[n] = p
                    heapq.heappush(todo, (tc, n))

        self.path = [self.end]
        curr = self.end
        while True:
            np = backtrack.get(curr)
            if np is None:
                break
            self.path.append(np)
            curr = np

    def find_cheats(self, cheat_duration: int) -> int:
        s = len(self.path)
        cheats: dict[int, int] = collections.defaultdict(int)

        # we "trim" path a->b (saved seconds) if distance between two points can
        # be reached within duration (1 tile/sec):
        #       #....a>>v#
        #       ########v#
        #       #....b<<<#
        for i in range(s - 1):
            for j in range(i + 35, s):
                a, b = self.path[i], self.path[j]
                distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
                if j - i > distance <= cheat_duration:
                    cheats[(j - i) - distance] += 1

        return sum(count for dur, count in cheats.items() if dur >= self.min_cheat_time)


@asserter
def part1(r: Racetrack) -> int:
    return r.find_cheats(2)


@asserter
def part2(r: Racetrack) -> int:
    return r.find_cheats(20)


@timing("day20")
def main() -> int:
    i = InputReader(2024, 20).raw

    example = Racetrack(i("example"), 30)
    puzzle = Racetrack(i("puzzle"), 100)

    def s1() -> None:
        assert part1(example)(4)
        assert part1(puzzle)(1452)

    def s2() -> None:
        assert part2(example)(881)
        assert part2(puzzle)(999556)

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
