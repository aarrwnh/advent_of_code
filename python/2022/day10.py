from support import assert_result, read_file_split, timing  # type: ignore


@timing()
def part1(lines: list[list[str]]) -> int:
    register = 1
    cycle = 1
    signal = 0

    for i in range(-2, len(lines)):
        pline = lines[i]

        for j in range(len(pline)):
            if j == 0 and pline[0] == "addx":
                register += int(pline[1])

            if cycle % 40 == 20:
                signal += cycle * register

            cycle += 1

    return signal


@timing()
def part2(lines: list[list[str]]) -> str:
    cycle = 1
    crt: list[list[str]] = [[] for _ in range(6)]
    row = 0
    sprite = 0
    # for cycle in range(1, 4 * 60 + 1):
    for i in range(-1, len(lines)):
        pline = lines[i]
        for j in range(len(pline)):
            if sprite - 1 < len(crt[row]) < sprite + 3:
                crt[row].append("#")
            else:
                crt[row].append(".")

            if j == 0 and pline[0] == "addx":
                sprite += int(pline[1])

            if cycle % 40 == 0:
                row += 1

            cycle += 1

        if cycle > 240:
            break

    return "\n".join(["".join(x) for x in crt]).replace("#", "█") + "\n\n"


part2_sample_res = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....\n
""".replace(
    "#", "█"
)

part2_puzzle_res = """###...##..###..#..#.###..####..##..###..
#..#.#..#.#..#.#..#.#..#.#....#..#.#..#.
#..#.#....#..#.####.###..###..#..#.###..
###..#.##.###..#..#.#..#.#....####.#..#.
#....#..#.#....#..#.#..#.#....#..#.#..#.
#.....###.#....#..#.###..####.#..#.###..\n
""".replace(
    "#", "█"
)


def main() -> int:
    sample = read_file_split(__file__, "../../input/2022/10/sample.input")
    puzzle = read_file_split(__file__, "../../input/2022/10/puzzle.input")

    assert_result(13140, part1(sample))
    assert_result(13520, part1(puzzle))

    assert_result(part2_sample_res, part2(sample))
    assert_result(part2_puzzle_res, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
