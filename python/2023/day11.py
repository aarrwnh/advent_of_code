from __future__ import annotations

from support import InputReader, Point, asserter, timing


class Universe:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.galaxies: list[Point] = []
        self.col_offsets: list[int] = []
        self.row_offsets: list[int] = []

    def new(self) -> Universe:
        row_has_galaxy: list[bool] = [False] * len(self.lines)

        row_offset = col_offset = 0

        for y, line in enumerate(self.lines):
            found_galaxy = False
            for x, ch in enumerate(line):
                if ch == "#":
                    found_galaxy = True
                    row_has_galaxy[x] = True
                    self.galaxies.append(Point(x, y))
            if not found_galaxy:
                row_offset += 1
            self.row_offsets.append(row_offset)

        for b in row_has_galaxy:
            if not b:
                col_offset += 1
            self.col_offsets.append(col_offset)

        self.universe_size = len(self.galaxies)

        return self

    def calc_distance(self, offset: int = 2) -> int:
        dist = 0
        offset = offset - 1

        for x, g1 in enumerate(self.galaxies):
            x_i = g1.x + self.col_offsets[g1.x] * offset
            y_i = g1.y + self.row_offsets[g1.y] * offset
            for _, g2 in enumerate(self.galaxies[1 + x : self.universe_size]):
                # print(f"{g1} {g2}")
                x_j = g2.x + self.col_offsets[g2.x] * offset
                y_j = g2.y + self.row_offsets[g2.y] * offset
                dist += abs(x_i - x_j) + abs(y_i - y_j)

        return dist


@asserter
@timing("part1")
def part1(u: Universe) -> int:
    return u.calc_distance(2)


@asserter
@timing("part2")
def part2(u: Universe, offset: int = 1) -> int:
    return u.calc_distance(offset)


def main() -> int:
    i = InputReader(2023, 11)

    sample = Universe(i.lines("sample")).new()
    puzzle = Universe(i.lines("puzzle")).new()

    part1(sample)(374)
    part1(puzzle)(9647174)

    part2(sample, 10)(1030)
    part2(sample, 100)(8410)
    part2(puzzle, 1000000)(377318892554)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
