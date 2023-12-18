import sys

from support import InputReader, asserter, timing


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    coords = {}
    x = 0
    y = 0
    coords[(x, y)] = "#"
    for line in lines:
        instruction, length_s, rgb = line.split(" ")
        dist = int(length_s)
        for _ in range(dist):
            match instruction:
                case "R":
                    x += 1
                case "L":
                    x -= 1
                case "D":
                    y += 1
                case "U":
                    y -= 1
            coords[(x, y)] = rgb

    min_x = min_y = sys.maxsize
    max_x = max_y = -sys.maxsize

    for p in coords:
        x, y = p
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    todo: list[tuple[int, int]] = []
    for x in range(min_x, max_x):
        if (x, min_y) in coords:
            todo.append((x + 1, min_y + 1))
            break

    while todo:
        p = todo.pop()
        if p in coords:
            continue
        else:
            coords[p] = "#"

        todo.append((p[0] - 1, p[1]))
        todo.append((p[0] + 1, p[1]))
        todo.append((p[0], p[1] + 1))
        todo.append((p[0], p[1] - 1))

    return len(coords.keys())


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    instructions = []
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for line in lines:
        _, _, rgb = line.split(" ")
        dist = int(rgb[2:7], 16)
        instruction = int(rgb[7:8])
        instructions.append((dist, dirs[instruction]))

    # Shoelace formula
    total = 0.0
    boundary = 0
    prev = (0, 0)
    for dist, dir in instructions:
        n = (prev[0] + dir[1] * dist, prev[1] + dir[0] * dist)
        total += ((prev[1] * n[0]) - (prev[0] * n[1])) / 2
        prev = n

        boundary += dist

    # Pick's theorem
    return int(total) + (boundary // 2) + 1


def main() -> int:
    i = InputReader(2023, 18).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(62)
        assert part1(puzzle)(68115)

    def s2() -> None:
        assert part2(sample)(952408144115)
        assert part2(puzzle)(71262565063800)

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
