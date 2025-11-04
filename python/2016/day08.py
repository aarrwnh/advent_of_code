import sys

from support import InputReader, asserter, timing

code = ""


@asserter
def part1(instructions: list[str], height: int, width: int) -> int:
    global code

    scr = [[False] * width for _ in range(height)]
    cand: set[int] = set()

    for inst in instructions:
        match inst.split(" "):
            case "rect", p:
                w, h = map(int, p.split("x"))
                for x in range(w):
                    for y in range(h):
                        scr[y][x] = True
            case "rotate", "row", row, "by", n_s:
                n = int(n_s)
                _, y_s = row.split("=")
                y = int(y_s)
                for x in range(width):
                    if scr[y][x]:
                        scr[y][x] = False
                        cand.add(x)
                for x in cand:
                    scr[y][(x + n) % width] = True
            case "rotate", "column", col, "by", n_s:
                n = int(n_s)
                _, x_s = col.split("=")
                x = int(x_s)
                for y in range(height):
                    if scr[y][x]:
                        scr[y][x] = False
                        cand.add(y)
                for y in cand:
                    scr[(y + n) % height][x] = True
            case _:
                raise AssertionError("unreachable")
        cand.clear()

    total = 0
    code = ""
    for y in range(height):
        for x in range(width):
            if scr[y][x]:
                total += 1
                code += "#"
            else:
                code += " "
        code += "\n"

    return total


@asserter
def part2() -> str:
    print(code)
    return "EOARGPHYAO"


@timing("day8")
def main() -> int:
    i = InputReader(2016, 8).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, 3, 7)(6)
        assert part1(puzzle, 6, 50)(128)

    def s2() -> None:
        assert part2()("EOARGPHYAO")

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
