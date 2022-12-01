from support import check_result, read_file, timing  # type: ignore


def compute(lines: list[str]) -> list[int]:
    calories: list[int] = []
    idx = 0
    prev = 0
    while idx < len(lines):
        if lines[idx] == "":
            calories.append(sum([int(x) for x in lines[prev:idx]]))
            prev = idx + 1
        idx += 1
    return sorted(calories)


@timing()
def part1(lines: list[str]) -> int:
    return compute(lines)[-1]


@timing()
def part2(lines: list[str]):
    return sum(compute(lines)[-3:])


def main() -> int:
    sample = read_file(__file__, "sample.input")
    puzzle = read_file(__file__, "puzzle.input")

    sample.append("")
    puzzle.append("")

    check_result(24000, part1(sample))
    check_result(71924, part1(puzzle))

    check_result(45000, part2(sample))
    check_result(210406, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
