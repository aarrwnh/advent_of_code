import os
from typing import List


def read_file(filename: str) -> List[str]:
    lines: List[str] = []
    path = os.path.dirname(
        __file__) + "/" + filename
    with open(path, "r") as f:
        for line in f.readlines():
            split = line.rstrip().split()
            lines.append(split[0])
    return lines


def get_most_bit_recurrences(arr: List[str]):
    half = len(arr) / 2 / 2
    line_len = len(arr[0])
    occ: List[int] = [0] * line_len
    for i in range(0, line_len):
        for line in arr:
            char = line[i]
            occ[i] += 1 if char == "1" else -1
            if occ[i] > half + 1 or occ[i] < -half - 1:
                break
    return occ


def to_bits(occ: List[int]) -> List[int]:
    for i, v in enumerate(occ):
        occ[i] = 1 if v >= 0 else 0
    return occ


def to_dec(bits: List[int]) -> int:
    return int("".join(map(lambda x: str(x), bits)), 2)


def flip_bits(bits: List[int]) -> List[int]:
    return [1 if x == 0 else 0 for x in bits]


def part1(lines: List[str]) -> int:
    occurrences = get_most_bit_recurrences(lines)
    bits = to_bits(occurrences)
    gamma = to_dec(bits)
    epsilon = to_dec(flip_bits(bits))
    return gamma * epsilon


def part2(lines: List[str]):
    oxygen = to_dec(filter_until_one(lines))
    co2 = to_dec(filter_until_one(lines, True))
    #  print(oxygen, co2)
    return oxygen * co2


def filter_until_one(lines: List[str], flip: bool = False) -> List[int]:
    linesize = len(lines[0])
    for i in range(0, linesize):
        filtered: List[str] = []
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


def main() -> None:
    sample = read_file("sample.input")
    lines = read_file("puzzle.input")

    print(part1(sample), 198)
    print(part2(sample), 230)

    print(part1(lines), 1025636)
    print(part2(lines), 793873)


if __name__ == "__main__":
    main()
