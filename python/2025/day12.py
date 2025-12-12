from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    chunks = input.split("\n\n")
    regions = [Region(s) for s in chunks.pop().splitlines()]
    shapes = [Shape(s) for s in chunks]

    return sum(
        r.area() >= sum(1 + n * shp.area for n, shp in zip(r.nums, shapes))
        for r in regions
    )


class Shape:
    area: int
    grid: dict[tuple[int, int], bool]

    def __init__(self, sh: str):
        i = 0
        g = {}
        for row, line in enumerate(sh.splitlines()[1:]):
            for col, ch in enumerate(line):
                if ch == "#":
                    g[row, col] = True
                    i += 1
        self.area = i
        self.grid = g


class Region:
    w: int
    h: int
    nums: list[int]

    def __init__(self, s: str) -> None:
        left, right = s.split(": ")
        w, h = map(int, left.split("x"))
        self.w = w
        self.h = h
        self.nums = list(map(int, right.split(" ")))

    def area(self) -> float:
        return float(self.w * self.h)

    def __repr__(self) -> str:
        return f"{self.w}x{self.h} {self.nums}"


@timing("day12")
def main() -> int:
    i = InputReader(2025, 12).raw

    assert part1(i("example"))(2)
    assert part1(i("puzzle"))(569)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
