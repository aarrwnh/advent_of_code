import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


class SeatCounter:
    def __init__(
        self, lines: list[str], *, adjacent_seats: bool = True, min_visible: int = 4
    ) -> None:
        self.min_visible = min_visible
        self.adjacent_seats = adjacent_seats
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])

    def _count_seats(self, x: int, y: int) -> int:
        assert self.lines is not None
        count = 0
        for dx, dy in self._adjacents(x, y):
            if self.lines[dy][dx] == "#":
                count += 1
        return count

    def _adjacents(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        assert self.lines is not None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                tx, ty = x, y
                while True:
                    tx += dx
                    ty += dy
                    if 0 <= ty < self.height and 0 <= tx < self.width:
                        if self.lines[ty][tx] != ".":
                            yield tx, ty
                            break
                    else:
                        break
                    # break after checking in proximity of one block
                    if self.adjacent_seats:
                        break

    def simulate(self) -> "SeatCounter":
        assert self.lines is not None
        prev = None
        while prev != self.lines:
            prev = self.lines
            new_lines = []
            for y, line in enumerate(self.lines):
                new_line = ""
                for x, p in enumerate(line):
                    if p == "L":
                        new_line += "#" if self._count_seats(x, y) == 0 else p
                    elif p == "#":
                        new_line += (
                            "L" if self._count_seats(x, y) >= self.min_visible else p
                        )
                    else:
                        new_line += p
                new_lines.append(new_line)
            self.lines = new_lines
        return self

    def count(self) -> int:
        return sum(line.count("#") for line in self.lines)


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    return SeatCounter(lines, min_visible=4).simulate().count()


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    return SeatCounter(lines, adjacent_seats=False, min_visible=5).simulate().count()


def main() -> int:
    i = InputReader(2020, 11).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(37)
        assert part1(puzzle)(2346)

    def s2() -> None:
        assert part2(sample)(26)
        assert part2(puzzle)(2111)

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
