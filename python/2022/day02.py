from support import assert_result, read_file_split, timing  # type: ignore

"""
A - rock    - X -- 1
B - paper   - Y -- 2
C - scissor - Z -- 3

6 - win
0 - loss
3 - draw
"""
POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}
RES = {
    "A": {"Z": -1, "Y": 1, "X": 0},
    "B": {"X": -1, "Z": 1, "Y": 0},
    "C": {"Y": -1, "X": 1, "Z": 0},
}
REV = {x: {v: k for k, v in RES[x].items()} for x in RES}


@timing()
def part1(rounds: list[list[str]]) -> int:
    total = 0
    for [elf, me] in rounds:
        p = RES[elf]
        if p[me] == 0:
            total += POINTS[me] + 3
        elif p[me] == 1:
            total += POINTS[me] + 6
        elif p[me] == -1:
            total += POINTS[me]
    return total


@timing()
def part2(rounds: list[list[str]]) -> int:
    """
    X -> lose
    Y -> draw
    Z -> win
    """
    total = 0
    for [elf, me] in rounds:
        p = REV[elf]
        if me == "Y":
            total += POINTS[p[0]] + 3
        elif me == "X":
            total += POINTS[p[-1]]
        elif me == "Z":
            total += POINTS[p[1]] + 6
    return total


def main() -> int:
    sample = [
        ["A", "Y"],
        ["B", "X"],
        ["C", "Z"],
    ]
    puzzle = read_file_split(__file__, "../../input/2022/02/puzzle.input")

    assert_result(15, part1(sample))
    assert_result(11841, part1(puzzle))

    assert_result(12, part2(sample))
    assert_result(13022, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
