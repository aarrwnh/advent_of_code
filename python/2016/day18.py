import sys

from support import InputReader, asserter, timing


@asserter
def count_safe(height: int, first_line: str) -> int:
    width = len(first_line)
    prev_line = 0
    count = 0
    mask = ((1 << width) - 1) << 1

    for c in first_line:
        prev_line |= 0 if c == "." else 1
        prev_line <<= 1

    #  .^^.^.^^^^
    # 0110101111_   << 1
    #  _0110101111  >> 1
    #  11100010011  L ^ R
    #  1110001001_  N & mask
    #  ^^^...^..^
    for _ in range(height):
        count += width - prev_line.bit_count()
        prev_line = ((prev_line << 1) ^ (prev_line >> 1)) & mask
    return count


@timing("day18")
def main() -> int:
    i = InputReader(2016, 18).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert count_safe(3, "..^^.")(6)
        assert count_safe(10, ".^^.^.^^^^")(38)
        assert count_safe(40, puzzle)(2035)

    def s2() -> None:
        assert count_safe(400_000, puzzle)(20_000_577)

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
