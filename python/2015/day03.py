import sys

from support import InputReader, asserter, timing

P = tuple[int, int]
DIRS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}


@asserter
def part1(moves: str) -> int:
    pos = (0, 0)
    visited: set[P] = set((pos,))
    for m in moves:
        dx, dy = DIRS[m]
        pos = pos[0] + dx, pos[1] + dy
        visited.add(pos)
    return len(visited)


@asserter
def part2(moves: str) -> int:
    pos = [(0, 0)] * 2
    visited: set[P] = set((pos[0],))

    def move(p: P, m: str) -> P:
        dx, dy = DIRS[m]
        p = p[0] + dx, p[1] + dy
        visited.add(p)
        return p

    for i, m in enumerate(moves):
        pos[i % 2] = move(pos[i % 2], m)

    return len(visited)


@timing("day03")
def main() -> int:
    i = InputReader(2015, 3).raw

    example = "^v^v^v^v^v"
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(2)
        assert part1(puzzle)(2081)

    def s2() -> None:
        assert part2(example)(11)
        assert part2(puzzle)(2341)

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
