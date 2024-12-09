import sys

from support import InputReader, asserter, timing

FREE = -1


@asserter
@timing("part1")
def part1(input: list[int]) -> int:
    disk_map: list[int] = []

    for idx, n in enumerate(input):
        v = idx // 2 if idx % 2 == 0 and n != 0 else FREE
        disk_map.extend([v] * n)

    a = 0
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


@asserter
@timing("part2")
def part2(input: list[int]) -> int:
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
