import sys

from support import check_result, read_file_raw, timing

# class Node:
#     def __init__(self, name: str) -> None:
#         self.name = name


def parse(input: str) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
    chunks = input.split("\n\n")
    seeds = [*map(int, chunks[0].split(": ")[1].split(" "))]
    data: list[list[tuple[int, int, int]]] = []
    for chunk in chunks[1:]:
        _, nums_s = chunk.split(" map:\n")
        # name_from, name_to = map_name.split("-to-")
        # nchild = data.setdefault(name_to, Node(name_to))
        # nfrom = data.setdefault(name_from, Node(name_from))
        # nfrom.child = nchild
        # nfrom.rows = []...
        c = []
        for nums in nums_s.rstrip().split("\n"):
            a = nums.split(" ")
            c.append((int(a[0]), int(a[1]), int(a[2])))
        data.append(c)
    return seeds, data


@timing("part1")
def part1(input: str) -> int:
    location = sys.maxsize
    seeds, data = parse(input)
    for seed in seeds:
        for maps in data:
            matches: set[int] = set()
            for map in maps:
                dest, src, r = map
                n = (seed - src) + dest
                if src <= seed <= src + r and dest <= n <= dest + r:
                    matches.add(n)
            if len(matches) == 0:
                matches.add(seed)
            seed = min(matches)
            matches.clear()
        location = min(location, seed)
    return location


def compute(
    depth: int, data: list[list[tuple[int, int, int]]], seed_start: int, seed_end: int
) -> int:
    if depth == 7:  # location
        return seed_start

    location = sys.maxsize
    ranges = [(seed_start, seed_end)]

    for dest, src, r in data[depth]:
        n = []

        for src_start, src_end in ranges:
            if src_end < src or src_start > src + r:
                n.append((src_start, src_end))
                continue

            dest_start = dest + max(src, src_start) - src
            dest_end = dest + min(src + r, src_end) - src

            a = compute(depth + 1, data, dest_start, dest_end)
            location = min(location, a)

            if src_start < src:
                n.append((src_start, src - 1))
            if src_end > src + r:
                n.append((src + r, src_end))

        ranges = n

    for src_start, src_end in ranges:
        a = compute(depth + 1, data, src_start, src_end)
        location = min(location, a)

    return location


@timing("part2")
def part2(input: str) -> int:
    seeds, data = parse(input)
    location = sys.maxsize
    for i in range(0, len(seeds), 2):
        seed_start, seed_range = seeds[i], seeds[i + 1]
        a = compute(0, data, seed_start, seed_start + seed_range)
        location = min(location, a)
    return location


@timing("part2")
def part2_brute(input: str) -> int:
    from multiprocessing import Pool

    seeds, data = parse(input)
    pairs = []
    for i in range(0, len(seeds), 2):
        pairs.append((seeds[i], seeds[i + 1], data))
    with Pool(4) as p:
        return min(p.map(ff, pairs))


def ff(x: tuple[int, int, list[list[tuple[int, int, int]]]]) -> int:
    location: set[int] = set()
    print("start seed: ", x[0])
    for seed in range(x[0], x[0] + x[1]):
        for maps in x[2]:
            matches: set[int] = set()
            for map in maps:
                dest, src, r = map
                n = (seed - src) + dest
                if src <= seed <= src + r and dest <= n <= dest + r:
                    matches.add(n)
            if len(matches) == 0:
                matches.add(seed)
            seed = min(matches)
            matches.clear()
        if len(location) == 0 or min(location) >= seed:
            location.add(seed)
    print("end seed:", x[0])
    return min(location)


def main() -> int:
    sample = read_file_raw(__file__, "../input/2023/05/sample")
    puzzle = read_file_raw(__file__, "../input/2023/05/puzzle")

    check_result(35, part1(sample))
    check_result(486613012, part1(puzzle))

    check_result(46, part2(sample))
    # check_result(46, part2_brute(sample))
    check_result(56931769, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
