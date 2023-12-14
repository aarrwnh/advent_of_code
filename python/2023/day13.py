from support import InputReader, asserter, timing


class Mirrors:
    def __init__(self, input: str) -> None:
        self.clusters: list[list[list[int]]] = []
        for cluster in input.split("\n\n"):
            grid: list[list[int]] = []
            for y, line in enumerate(cluster.splitlines()):
                grid.append([])
                for _, p in enumerate(line):
                    grid[y].append(ord(p))
            self.clusters.append(grid)

    def find_horizontal(
        self, y1: int, y2: int, cluster: list[list[int]], smuges: int = -1
    ) -> tuple[bool, int]:
        for x in range(len(cluster[0])):
            if cluster[y1][x] != cluster[y2][x]:
                if smuges > -1:
                    smuges += 1
                else:
                    return False, smuges
        if y1 > 0 and y2 + 1 < len(cluster):
            return self.find_horizontal(y1 - 1, y2 + 1, cluster, smuges)
        return True, smuges

    def find_vertical(
        self, x1: int, x2: int, cluster: list[list[int]], smuges: int = -1
    ) -> tuple[bool, int]:
        for y in range(len(cluster)):
            if cluster[y][x1] != cluster[y][x2]:
                if smuges > -1:
                    smuges += 1
                else:
                    return False, smuges
        if x1 > 0 and x2 + 1 < len(cluster[0]):
            return self.find_vertical(x1 - 1, x2 + 1, cluster, smuges)
        return True, smuges


class MirrorBits:
    def __init__(self, input: str) -> None:
        self.clusters: list[tuple[list[int], ...]] = []
        for cluster in input.split("\n\n"):
            lines = cluster.splitlines()
            width = len(lines[0])
            row_masks: list[int] = []
            col_masks: list[int] = [0] * width
            for row, line in enumerate(lines):
                row_masks.append(0)
                for col, p in enumerate(line):
                    if p == "#":
                        row_masks[row] |= 1 << col
                        col_masks[col] |= 1 << row
            self.clusters.append((row_masks, col_masks))

    def find_mirrors(self, masks: list[int], n: int = 0) -> int:
        size = len(masks)
        # find at least two matching pairs
        for i in range(size - 1):
            diff = (masks[i] ^ masks[i + 1]).bit_count()
            if diff <= n:
                # print(i, f"{val1:10b} => {val2:10b}", val1, val2)
                for j1 in range(max((2 * i + 2) - size, 0), i):
                    j2 = 2 * i - j1 + 1
                    diff += (masks[j1] ^ masks[j2]).bit_count()
                    if diff > n:
                        break
                if diff == n:
                    return i + 1
        return 0


@asserter
@timing("part1")
def part1_1(m: Mirrors) -> int:
    total = 0
    for cluster in m.clusters:
        for y in range(len(cluster) - 1):
            if m.find_horizontal(y, y + 1, cluster)[0]:
                total += (y + 1) * 100
        for x in range(len(cluster[0]) - 1):
            if m.find_vertical(x, x + 1, cluster)[0]:
                total += x + 1
    return total


@asserter
@timing("part2")
def part2_1(m: Mirrors) -> int:
    total = 0
    for cluster in m.clusters:
        for y in range(len(cluster) - 1):
            if m.find_horizontal(y, y + 1, cluster, 0) == (True, 1):
                total += (y + 1) * 100
        for x in range(len(cluster[0]) - 1):
            if m.find_vertical(x, x + 1, cluster, 0) == (True, 1):
                total += x + 1
    return total


@asserter
@timing("part1_2")
def part1_2(m: MirrorBits) -> int:
    total = 0
    for rowm, colm in m.clusters:
        total += 100 * m.find_mirrors(rowm, 0)
        total += m.find_mirrors(colm, 0)
    return total


@asserter
@timing("part2_2")
def part2_2(m: MirrorBits) -> int:
    total = 0
    for rowm, colm in m.clusters:
        total += 100 * m.find_mirrors(rowm, 1)
        total += m.find_mirrors(colm, 1)
    return total


@timing("main")
def main() -> int:
    i = InputReader(2023, 13)

    sample_s, puzzle_s = i.raw("sample"), i.raw("puzzle")

    sample, puzzle = Mirrors(sample_s), Mirrors(puzzle_s)

    part1_1(sample)(405)
    part1_1(puzzle)(34821)

    part2_1(sample)(400)
    part2_1(puzzle)(36919)

    sample_2, puzzle_2 = MirrorBits(sample_s), MirrorBits(puzzle_s)

    part1_2(sample_2)(405)
    part1_2(puzzle_2)(34821)

    part2_2(sample_2)(400)
    part2_2(puzzle_2)(36919)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
