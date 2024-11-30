import collections
import sys

from support import InputReader, Point, asserter, timing

P = tuple[int, int]
A = tuple[P, int, P, P, int]


DIRECTIONS: dict[P, str] = {
    (1, 0): ">",
    (-1, 0): "<",
    (0, 1): "v",
    (0, -1): "^",
}


class Maze:
    def __init__(self, g: tuple[dict[Point, str], int, int, Point]) -> None:
        grid, width, height, _ = g
        self.route = {(k[0], k[1]): v for k, v in grid.items() if v != "#"}
        self.start = (1, 0)
        self.end = (width - 2, height - 1)

        # edges
        self.intersections: collections.defaultdict[P, set[tuple[P, int]]]
        self.intersections = collections.defaultdict(set)

    def long_walk(self) -> int:
        start_pos: A = (self.start, 0, self.start, (0, 1), 0)
        todo: collections.deque[A]
        todo = collections.deque([start_pos])

        self.intersections.clear()

        max_dist = 0

        while todo:
            lastpos, lastdist, curpos, curdir, dist = todo.popleft()

            if curpos == self.end:
                max_dist = max(max_dist, dist)
                self.intersections[lastpos].add((self.end, dist - lastdist))
                continue

            possible = 0
            candidates: list[tuple[P, P, int]] = []
            for dx, dy in DIRECTIONS:
                if (-dx, -dy) == curdir:
                    continue

                nextpos = curpos[0] + dx, curpos[1] + dy
                if nextpos in self.route:
                    ch = self.route[nextpos]
                    if ch == ".":
                        candidates.append((nextpos, (dx, dy), dist + 1))
                    else:
                        possible += 1
                        if DIRECTIONS[(dx, dy)] == ch:
                            candidates.append((nextpos, (dx, dy), dist + 1))

            saved_pos = lastpos
            saved_dist = lastdist
            if possible > 1:
                # path  A -> B
                self.intersections[curpos].add((lastpos, dist - lastdist))
                # path  B -> A
                self.intersections[lastpos].add((curpos, dist - lastdist))
                saved_pos = curpos
                saved_dist = dist

            for cand in candidates:
                todo.append((saved_pos, saved_dist, *cand))

        return max_dist

    def scenic_hike(self) -> int:
        self.long_walk()

        todo: collections.deque[tuple[P, int, set[P]]]
        todo = collections.deque([(self.start, 0, set())])

        max_dist = 0

        while todo:
            curpos, dist, visited = todo.pop()
            if self.end == curpos:
                max_dist = max(max_dist, dist)
                continue

            if curpos in visited:
                continue
            visited.add(curpos)

            for nextpos, nextdist in self.intersections[curpos]:
                todo.append((nextpos, nextdist + dist, visited.copy()))

        return max_dist


@asserter
@timing("part1")
def part1(m: Maze) -> int:
    return m.long_walk()


@asserter
@timing("part2")
def part2(m: Maze) -> int:
    return m.scenic_hike()


def main() -> int:
    i = InputReader(2023, 23).grid

    sample = Maze(i("sample"))
    puzzle = Maze(i("puzzle"))

    def s1() -> None:
        assert part1(sample)(94)
        assert part1(puzzle)(2030)

    def s2() -> None:
        assert part2(sample)(154)
        assert part2(puzzle)(6390)

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
