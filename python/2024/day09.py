import sys

from support import InputReader, asserter, timing

FREE = -1


@asserter
def part1(input: list[int]) -> int:
    disk_map: list[int] = []

    for idx, n in enumerate(input):
        v = idx // 2 if idx % 2 == 0 and n != 0 else FREE
        disk_map.extend([v] * n)

    a = 2  # disk_map.index(FREE)
    b = len(disk_map) - 1
    total = 0
    while b >= a:
        file = disk_map[a]
        if file == FREE:
            # from end
            file = disk_map.pop(b)
            b -= 1
            if file == FREE:
                continue
        total += a * file
        a += 1

    return total


class Block:
    def __init__(self, start: int, size: int, idx: None | int = None) -> None:
        self.start = start
        self.length = size
        self.idx = idx

    def checksum(self) -> int:
        idx = self.idx if self.idx else 0
        stop = self.start + self.length
        return sum([*range(self.start, stop)]) * idx

    def __repr__(self) -> str:
        return f"({self.start}, {self.length}, {self.idx})"


@asserter
def part2(input: list[int]) -> int:
    def sort_start(b: Block) -> int:
        return b.start

    files: list[Block] = []
    free_space: list[list[Block]] = [[] for _ in range(10)]

    start_block = 0
    for idx, length in enumerate(input):
        if length > 0:
            if idx % 2 == 0:
                files.append(Block(start_block, length, idx // 2))
            else:
                free_space[length].append(Block(start_block, length))
        start_block += length

    for idx in range(len(files) - 1, -1, -1):
        length = files[idx].length
        start = files[idx].start

        free: set[Block] = set()
        for free_list in free_space[length:]:
            if free_list and free_list[0].start < start:
                free.add(free_list[0])

        if not free:
            continue

        free0 = min(free, key=sort_start)
        free0 = free_space[free0.length].pop(0)
        files[idx].start = free0.start

        if free0.length > length:
            free0.length -= length
            free0.start += length

            try:
                free_space[free0.length].index(free0)
            except Exception as _:
                v = free_space[free0.length]
                v.append(free0)
                free_space[free0.length] = sorted(v, key=sort_start)

    return sum(f.checksum() for f in files)


@asserter
def part2_brute(input: list[int]) -> int:
    disk_map: list[list[int]] = []

    for idx, n in enumerate(input):
        if n != 0:
            v = idx // 2 if idx % 2 == 0 else FREE
            disk_map.append([v] * n)

    start = 0
    end = len(disk_map) - 1

    # go by blocks from end and try to fit in empty spaces from front
    while end >= 0:
        src = disk_map[end]
        size = len(src)
        end -= 1

        # skip on just empty chunk
        if src.count(FREE) == size:
            continue

        found = False
        # scan each time and look for empty space
        for j in range(start, end + 1):
            dest = disk_map[j]
            empty_slots = dest.count(FREE)

            # change index to leftmost chunk with empty slots
            if not found and empty_slots > 0:
                start = j
                found = True

            # drain src block
            if empty_slots >= size:
                x = 0
                for idx, val in enumerate(dest):
                    if val == FREE and x < size:
                        dest[idx], src[x], x = src[x], FREE, x + 1
                break

    total = 0
    idx = 0
    for chunk in disk_map:
        for n in chunk:
            if n != FREE:
                total += idx * n
            idx += 1

    return total


@timing("day9")
def main() -> int:
    i = InputReader(2024, 9).numbers

    example = i("example")[0]
    puzzle = i("puzzle")[0]

    def s1() -> None:
        assert part1(example)(1928)
        assert part1(puzzle)(6398252054886)

    def s2() -> None:
        assert part2(example)(2858)
        assert part2(puzzle)(6415666220005)

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
