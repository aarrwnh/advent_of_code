from typing import Dict, List, Set
import os
from support import timing

unique_numbers = (-1, -1, 1, 7, 4, -1, -1, 8)


def read_file(filename: str) -> List[str]:
    path = os.path.dirname(__file__) + "/" + filename
    return [line.rstrip() for line in open(path, "r").readlines()]


def parse_line(left_words: List[str], right_words: List[str]) -> int:
    words: set[str] = set([*map(lambda x: "".join(sorted(x, key=None)), left_words)])
    decipher: Dict[int, set[str]] = {}

    def update_cipher(dest: int, word: Set[str], check: bool):
        if check:
            decipher[dest] = word

    size_5_words: List[Set[str]] = []
    size_6_words: List[Set[str]] = []
    for word in set(words):
        word_len = len(word)
        word = set(word)
        if unique_numbers[word_len] != -1:
            decipher[unique_numbers[word_len]] = word
        elif word_len == 5:
            size_5_words.append(word)
        elif word_len == 6:
            size_6_words.append(word)

    for word in size_6_words:
        update_cipher(9, word, len(word & decipher[4]) == 4)
        update_cipher(6, word, len(word & decipher[1]) == 1)
        update_cipher(0, word, len((word - decipher[7]) & decipher[4]) == 1)
    for word in size_5_words:
        update_cipher(3, word, len(word & decipher[7]) == 3)
        update_cipher(2, word, len(word & decipher[4]) == 2)
        update_cipher(5, word, len((word - decipher[7]) & decipher[4]) == 2)

    digits: List[str] = []
    for word in right_words:
        for i in decipher:
            if decipher[i] == set(word):
                digits.append(str(i))
                break

    return int("".join(digits))


@timing()
def part1(lines: List[str]) -> int:
    u = set(i for i, n in enumerate(unique_numbers) if n != -1)
    unique: int = 0
    for line in lines:
        _, right = line.split(" | ")
        right = right.split("\x20")
        unique += len([x for x in right if len(x) in u])
    return unique


@timing()
def part2(lines: List[str]) -> int:
    count: int = 0
    for line in lines:
        left, right = line.split(" | ")
        left = left.split("\x20")
        right = right.split("\x20")
        count += parse_line(left, right)
    return count


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    example = read_file("sample.input")
    example2 = read_file("sample2.input")
    puzzle = read_file("puzzle.input")

    check_result(26, part1(example))
    check_result(310, part1(puzzle))

    check_result(5353, part2(example2))
    check_result(61229, part2(example))
    check_result(915941, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
