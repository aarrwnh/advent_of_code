import sys

from support import assert_result, read_file_raw, timing

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
        data.append(sorted(c, key=lambda x: x[1]))
    return seeds, data


@timing("part1")
def part1(input: str) -> int:
    seeds, maps = parse(input)
    for row in maps:
        matches: list[int] = []
        for seed in seeds:
            for dest, src, r in row:
                if src <= seed < src + r:
                    matches.append(seed - src + dest)
                    break
            else:
                matches.append(seed)
        seeds = matches
    return min(seeds)


@timing("part2")
def part2_1(input: str) -> int:
    def compute(
        depth: int,
        data: list[list[tuple[int, int, int]]],
        seed_start: int,
        seed_end: int,
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

    seeds, data = parse(input)
    location = sys.maxsize
    for i in range(0, len(seeds), 2):
        a = compute(0, data, seeds[i], seeds[i] + seeds[i + 1])
        location = min(location, a)
    return location


@timing("part2_2")
def part2_2(input: str) -> int:
    seeds, data = parse(input)
    cur_ranges = []

    for i in range(0, len(seeds), 2):
        seed_start, seed_range = seeds[i], seeds[i + 1]
        cur_ranges.append((seed_start, seed_start + seed_range))

    for map in data:
        n: list[tuple[int, int]] = []
        for r_start, r_end in cur_ranges:
            for dest, src, r in map:
                src_range_end = src + r
                offset = dest - src
                # in range
                if src <= r_start < src_range_end and src <= r_end < src_range_end:
                    n.append((r_start + offset, r_end + offset))
                    break
                # cut left
                elif src <= r_start < src_range_end:
                    n.append((r_start + offset, dest + r))
                    r_start = src + r
                elif r_start <= src < r_end and r_start <= src_range_end < r_end:
                    n.append((r_start, src))
                    n.append((dest, dest + r))
                    r_start = src + r
                # cut right
                elif r_start <= src < r_end:
                    n.append((r_start, src))
                    n.append((dest, dest + r_end - src))
                    break
            else:
                n.append((r_start, r_end))

        cur_ranges = n

    return min(min(cur_ranges))


@timing("part2")
def part2_brutal(input: str, proc: str = "0") -> int:
    from multiprocessing import Pool, cpu_count

    seeds, data = parse(input)
    pairs = []
    cc = cpu_count() if proc == "0" else int(proc)
    for i in range(0, len(seeds), 2):
        pairs.append((seeds[i], seeds[i + 1], data))
    with Pool(cc) as p:
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
    sample = read_file_raw(__file__, "../../input/2023/05/sample")
    puzzle = read_file_raw(__file__, "../../input/2023/05/puzzle")

    assert_result(35, part1(sample))
    assert_result(486613012, part1(puzzle))

    if len(sys.argv) == 2:
        print("!!!!BRUTE FORCE!!!!", sys.argv[1])  # ~10 mins / 4 cores
        assert_result(46, part2_brutal(sample, sys.argv[1]))
        assert_result(56931769, part2_brutal(puzzle, sys.argv[1]))
    else:
        assert_result(46, part2_1(sample))
        assert_result(56931769, part2_1(puzzle))

        assert_result(46, part2_2(sample))
        assert_result(56931769, part2_2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
