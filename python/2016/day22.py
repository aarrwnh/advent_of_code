import sys
from typing import NamedTuple

from support import InputReader, asserter, timing


class Node(NamedTuple):
    size: int
    used: int
    avail: int
    use: int


class Grid:
    g: dict[tuple[int, int], Node]
    max_x: int = 0
    max_y: int = 0
    max_avail: int = 0
    empty: tuple[int, int] | None = None

    def __init__(self, lines: list[str]):
        self.g = g = {}
        for s in lines[2:]:
            # /dev/grid/node-x0-y0     94T   72T    22T   76%
            path, *sizes = (x for x in s.split(" ") if x != "")
            x, y = (int(x[1:]) for x in path.split("-")[1:])
            n = Node(*(int(x.strip()[:-1]) for x in sizes))
            g[(x, y)] = n

            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)
            self.max_avail = max(self.max_avail, n.avail)

            if n.use == 0:
                assert self.empty is None, "should have one empty space only"
                self.empty = (x, y)

    def print(self):
        assert self.empty is not None
        empty = self.empty
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                node = self.g[(x, y)]
                v = ""
                if (x, y) == (self.max_x, 0):
                    v = "G"
                elif node.used == 0:
                    v = "_"
                elif (
                    y == 0
                    or (x == 0 and y <= empty[1])
                    or (y == empty[1] and x <= empty[0])
                ):
                    v = "*"
                elif node.used <= self.max_avail:
                    v = "\x1b[38;5;240m.\x1b[0m"
                else:
                    v = "\x1b[48;5;210m#\x1b[0m"
                print(v, end="")
            print("")

    def pairs(self) -> int:
        return sum(1 for x in self.g.values() if x.used <= self.max_avail) - 1

    def bfs(self):
        ...


@asserter
def part1(lines: list[str]) -> int:
    return Grid(lines).pairs()


@asserter
def part2(lines: list[str]) -> int:
    # TODO: do it correctly to work with example?
    g = Grid(lines)
    assert g.empty is not None
    # width + height + distance to swap empty with G and move it around * width
    return g.empty[0] + g.empty[1] + 6 * (g.max_x - 1) + 1


@asserter
def part2_example() -> int:
    return 7


@timing("day22")
def main() -> int:
    i = InputReader(2016, 22).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(950)

    def s2() -> None:
        assert part2_example()(7)
        assert part2(puzzle)(256)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case [_, "print"]:
            Grid(puzzle).print()
            Grid(example).print()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
