from typing import Dict, List, Set
import os
from support import timing


def read_file(filename: str) -> List[str]:
    path = os.path.dirname(__file__) + "/" + filename
    return [line.rstrip() for line in open(path, "r").readlines()]


def very_brute_force_because_i_was_bored(
    left_words: List[str], right_words: List[str]
) -> int:
    digits_decoded: Dict[int, int] = {}
    left_words = set(sorted(left_words, key=len))
    dis = {2: 1, 3: 7, 4: 4, 7: 8}

    #  filter_unique
    for word in list(left_words):
        if len(word) in (2, 3, 4, 7):
            no = dis[len(word)]
            digits_decoded[word] = no
            digits_decoded[no] = word
            left_words -= set([word])

    top = set(digits_decoded[7]) - set(digits_decoded[1])

    # example outputs
    # . d .
    # e . a
    # . f .
    # g . b
    # . c .

    # top line
    # x x x
    # x . x
    # x x x
    # . . x
    # . . x
    four_top = set(digits_decoded[4])
    four_top.update(top)

    # . . .
    # . . .
    # . . .
    # x . .
    # x x .
    eight_left = set(digits_decoded[8]) - four_top

    # . . .
    # . . .
    # . . .
    # . . .
    # x x x
    bottom = set()
    for word in list(left_words):
        if len(word) == 5:
            one_letter = set(word) - four_top
            if len(one_letter) == 1:
                bottom = one_letter
                break

    # . . .
    # . . .
    # x . .
    # x . .
    # x . .
    bottom_left = eight_left - bottom

    nine = set()
    for word in list(left_words):
        if len(word) == 6:
            temp_word = set(word) - top - bottom
            if temp_word == set(digits_decoded[4]):
                nine = set(word)
                left_words -= set([word])
                break

    # x . .
    # x . .
    # x x x
    # . . .
    # x x x
    nine_minus_seven = nine - set(digits_decoded[7])

    five = set()
    for word in list(left_words):
        if len(word) == 5:
            temp_word = nine - set(digits_decoded[1]) - set(word)
            #  temp_word.update(bottom_left)
            if len(temp_word) == 0:
                five = set(word)
                left_words -= set([word])

    # x . .
    # x . .
    # x . .
    # . . .
    # . . .
    top_left = set()
    two = set()
    for word in left_words:
        if len(word) == 5:
            temp_word = five - set(word)
            if len(temp_word) == 1:
                two = set(word)
                top_left.update(temp_word)

    zero = set(digits_decoded[7])
    zero.update(top_left)
    zero.update(eight_left)

    # . . .
    # . . .
    # x x x
    # . . .
    # . . .
    middle = set(digits_decoded[8]) - zero

    # . . x
    # . . x
    # . . x
    # . . .
    # . . .
    top_right = set(digits_decoded[8]) - five - bottom_left

    # . . .
    # . . .
    # . . x
    # . . x
    # . . x
    bottom_right: set[int] = set(digits_decoded[1]) - top_right

    two = set(digits_decoded[8]) - top_left - bottom_right
    three = nine - top_left
    six = set(digits_decoded[8]) - top_right

    digits_decoded[0] = zero
    digits_decoded[5] = five
    digits_decoded[9] = nine
    digits_decoded[2] = two
    digits_decoded[3] = three
    digits_decoded[6] = six

    cleaned_digits_decoded = {}
    for di in digits_decoded:
        if type(di) == int:
            val = sorted([*digits_decoded[di]])
            cleaned_digits_decoded["".join(val)] = di

    #  pprint(cleaned_digits_decoded)

    def swap_letters_to_index(scrambled_letters: str) -> int:
        word = "".join(sorted([*scrambled_letters]))
        try:
            return str(cleaned_digits_decoded[word])
        except Exception:
            print(word)
            pprint(cleaned_digits_decoded)
            return str(0)

    char_results = []
    for char in right_words:
        char_results.append(swap_letters_to_index(char))
    return int("".join(char_results))


@timing()
def part1(lines: List[str]) -> int:
    some_count = 0
    for line in lines:
        _, right = line.split(" | ")
        some_count += len([x for x in right.split("\x20") if len(x) in {2, 3, 4, 7}])
    return some_count


@timing()
def part2(lines: List[str]):
    results = []
    for line in lines:
        left, right = line.split(" | ")
        left = left.split("\x20")
        right = right.split("\x20")
        results.append(very_brute_force_because_i_was_bored(left, right))
    return sum(results)


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    example = read_file("sample.input")
    example2 = read_file("sample2.input")
    puzzle = read_file("puzzle.input")

    check_result(26, part1(example))
    check_result(310, part1(puzzle))

    check_result(61229, part2(example))
    check_result(5353, part2(example2))
    check_result(915941, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
