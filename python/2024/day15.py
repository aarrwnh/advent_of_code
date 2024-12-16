import sys

from support import InputReader, asserter, timing

DIRS = {
    "^": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
}

P = tuple[int, int]
G = dict[P, str]


class Warehouse:
    def __init__(self, input: str):
        self.grid: G = {}
        self.start_pos = (0, 0)
        self._parse(input)

    def _parse(self, input: str) -> None:
        a, b = input.split("\n\n")
        self.moves = "".join(b.split("\n"))

        for y, row in enumerate(a.split("\n")):
            for x, p in enumerate(row.strip()):
                if p == "@":
                    self.start_pos = (x, y)
                elif p == "#" or p == "O":
                    self.grid[(x, y)] = p

    def _move_once(
        self, todo: list[P], queued_boxes: dict[P, str], dx: int, dy: int
    ) -> bool:
        def push(next: list[P], ch: str, n: P) -> None:
            if n not in queued_boxes:
                queued_boxes[n] = ch
                next.append(n)

        while True:
            next: list[P] = []

            for px, py in todo:
                n = px + dx, py + dy

                if n not in self.grid:
                    continue

                match self.grid[n]:
                    case "#":
                        # continue to next move
                        return False
                    case "O":
                        push(next, "O", n)
                    case "[":
                        push(next, "[", n)
                        push(next, "]", (n[0] + 1, n[1]))
                    case "]":
                        push(next, "]", n)
                        push(next, "[", (n[0] - 1, n[1]))
                    case _:
                        raise AssertionError("unknown char")

            if not next:
                break

            todo = next
        return True

    def move_robot(self) -> "Warehouse":
        x, y = self.start_pos
        for move in self.moves:
            dx, dy = DIRS[move]
            todo: list[P] = [(x, y)]
            queued_boxes: dict[P, str] = {}
            if not self._move_once(todo, queued_boxes, dx, dy):
                continue
            self._move_boxes(queued_boxes, dx, dy)
            x, y = x + dx, y + dy

        return self

    def _move_boxes(self, boxes: dict[P, str], dx: int, dy: int) -> None:
        for m, _ in boxes.items():
            self.grid.pop(m)

        for n, ch in boxes.items():
            self.grid[(n[0] + dx, n[1] + dy)] = ch

    def gps_sum(self) -> int:
        total = 0
        for p in self.grid:
            if self.grid[p] == "O" or self.grid[p] == "[":
                total += p[1] * 100 + p[0]
        return total


# @asserter
# def part1_1(input: str) -> int:
#     g, moves = parse(input)
#     grid, start_pos, max_x, max_y = g.grid, g.start_pos, g.max_x, g.max_y
#     x, y = start_pos
#     grid[(x, y)] = EMPTY
#     for move in moves:
#         dx, dy = DIRS[move]
#         nx, ny = x + dx, y + dy
#         if grid[(nx, ny)] == EMPTY:
#             x, y = nx, ny
#         else:
#             cx, cy = x + dx, y + dy
#             to_move: list[tuple[int, int]] = []
#             while 0 < cx < max_x and 0 < cy < max_y and grid[(cx, cy)] != WALL:
#                 if grid[(cx, cy)] == EMPTY:
#                     bx, by = to_move.pop()
#                     grid[(nx, ny)] = EMPTY
#                     grid[(bx + dx, by + dy)] = BOX
#                     x, y = nx, ny
#                     break
#                 to_move.append((cx, cy))
#                 cx, cy = cx + dx, cy + dy
#     return gps(grid)


@asserter
def part1(input: str) -> int:
    return Warehouse(input).move_robot().gps_sum()


@asserter
def part2(input: str) -> int:
    r = Warehouse(input)
    r.start_pos = (r.start_pos[0] * 2, r.start_pos[1])

    new_grid: G = {}
    for p in r.grid:
        ch = r.grid[p]
        x, y = p
        if ch == "#":
            new_grid[(x * 2, y)] = ch
            new_grid[(1 + x * 2, y)] = ch
        elif ch == "O":
            new_grid[(x * 2, y)] = "["
            new_grid[(1 + x * 2, y)] = "]"
    r.grid = new_grid

    return r.move_robot().gps_sum()


@timing("day15")
def main() -> int:
    i = InputReader(2024, 15).raw

    example = i("example")
    example2 = i("example2")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example2)(10092)
        assert part1(puzzle)(1478649)

    def s2() -> None:
        assert part2(example)(618)
        assert part2(example2)(9021)
        assert part2(puzzle)(1495455)

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
