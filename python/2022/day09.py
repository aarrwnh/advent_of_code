import math

from support import check_result, read_file_lines, timing  # type: ignore

MOVEMENTS: dict[str, tuple[int, int]] = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}


@timing()
def part1(lines: list[str]) -> int:
    start = (0, 0)
    head_pos = tail_pos = start
    tail_visited: set[tuple[int, int]] = {start}
    # tail_visited: collections.Counter[tuple[int, int]] = collections.Counter()
    for line in lines:
        direction, a = line.split()
        for _ in range(int(a)):
            head_next_x, head_next_y = MOVEMENTS[direction]
            prev_head_pos = head_pos
            head_pos = (head_pos[0] + head_next_x, head_pos[1] + head_next_y)
            # abs(head_pos[1] - tail_pos[1]) >= 2
            if math.hypot(head_pos[1] - tail_pos[1], head_pos[0] - tail_pos[0]) >= 2:
                tail_pos = prev_head_pos
                tail_visited.add(tail_pos)

    return len(tail_visited)


def adjust_knots(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    tx, ty = tail
    hx, hy = head
    dist_y = abs(hy - ty)
    dist_x = abs(hx - tx)
    if dist_x == 2 and dist_y == 2:
        return ((hx + tx) // 2, (hy + ty) // 2)
    elif dist_y == 2:
        return (hx, (hy + ty) // 2)
    elif dist_x == 2:
        return ((hx + tx) // 2, hy)
    return tail


@timing()
def part2(lines: list[str]):
    start = (0, 0)
    head_pos = start
    path: list[tuple[int, int]] = [start] * 10

    tail_visited: set[tuple[int, int]] = {start}

    for line in lines:
        direction, a = line.split()
        for _ in range(int(a)):
            head_next_x, head_next_y = MOVEMENTS[direction]

            head_pos = (head_pos[0] + head_next_x, head_pos[1] + head_next_y)
            path[0] = prev_head_pos = head_pos

            for idx in range(1, len(path)):
                new_pos = adjust_knots(prev_head_pos, path[idx])
                path[idx] = prev_head_pos = new_pos

            tail_visited.add(path[-1])

    return len(tail_visited)


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/09/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/09/puzzle.input")
    sample2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""".strip().split(
        "\n"
    )

    check_result(13, part1(sample))
    check_result(6175, part1(puzzle))

    check_result(1, part2(sample))
    check_result(36, part2(sample2))
    check_result(2578, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
