from support import assert_result, read_file, timing


def get_most_bit_recurrences(arr: list[str]) -> list[int]:
    half = len(arr) / 2 / 2
    line_len = len(arr[0])
    occ: list[int] = [0] * line_len
    for i in range(0, line_len):
        for line in arr:
            char = line[i]
            occ[i] += 1 if char == "1" else -1
            if occ[i] > half + 1 or occ[i] < -half - 1:
                break
    return occ


def to_bits(occ: list[int]) -> list[int]:
    for i, v in enumerate(occ):
        occ[i] = 1 if v >= 0 else 0
    return occ


def to_dec(bits: list[int]) -> int:
    return int("".join(map(lambda x: str(x), bits)), 2)


def flip_bits(bits: list[int]) -> list[int]:
    return [1 if x == 0 else 0 for x in bits]


@timing()
def part1(lines: list[str]) -> int:
    occurrences = get_most_bit_recurrences(lines)
    bits = to_bits(occurrences)
    gamma = to_dec(bits)
    epsilon = to_dec(flip_bits(bits))
    return gamma * epsilon


@timing()
def part2(lines: list[str]) -> int:
    oxygen = to_dec(filter_until_one(lines))
    co2 = to_dec(filter_until_one(lines, True))
    #  print(oxygen, co2)
    return oxygen * co2


def filter_until_one(lines: list[str], flip: bool = False) -> list[int]:
    linesize = len(lines[0])
    for i in range(0, linesize):
        filtered: list[str] = []
        occurrences = get_most_bit_recurrences(lines)
        bits = to_bits(occurrences)
        expected_bits = list(map(lambda x: str(x), flip_bits(bits) if flip else bits))

        for line in lines:
            if line[i] == expected_bits[i]:
                filtered.append(line)

        lines = filtered
        if len(lines) == 1:
            return [int(x) for x in lines[0]]
    return [0]


def main() -> int:
    sample = read_file(__file__, "sample.input")
    lines = read_file(__file__, "puzzle.input")

    assert_result(198, part1(sample))
    assert_result(230, part2(sample))

    assert_result(1025636, part1(lines))
    assert_result(793873, part2(lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
