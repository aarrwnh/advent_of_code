from support import assert_result, read_file_split, timing


def accumulate(arr: list[list[str]], check_visited: bool = True) -> int:
    idx: int = 0
    acc: int = 0
    visited: list[int] = []
    while True:
        if idx >= len(arr):
            return acc
        if idx in visited:
            return acc if check_visited else False

        visited.append(idx)
        method, value_s = arr[idx]
        value = int(value_s)

        if method == "nop":
            idx += 1
        elif method == "jmp":
            idx += value
        elif method == "acc":
            idx += 1
            acc += value


@timing()
def part1(arr: list[list[str]], part1: bool = True) -> int:
    return accumulate(arr, part1)


@timing()
def part2(lines: list[list[str]]):
    for idx, line in enumerate(lines):
        method = line[0]
        if method == "nop" or line[0] == "jmp":
            prev = method
            lines[idx][0] = "nop" if method == "jmp" else "jmp"
            if accumulator := accumulate(lines, False):
                return accumulator
            lines[idx][0] = prev


def main() -> int:
    sample = read_file_split(__file__, "../../input/2020/08/sample.input")
    puzzle = read_file_split(__file__, "../../input/2020/08/puzzle.input")

    assert_result(5, part1(sample))
    assert_result(1832, part1(puzzle))

    assert_result(8, part2(sample))
    assert_result(662, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
