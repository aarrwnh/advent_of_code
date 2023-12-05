from typing import List
import os
from pprint import pprint
import math
from support import timing


def read_file(filename: str) -> List[str]:
    lines: List[str] = []
    path = os.path.dirname(__file__) + "/" + filename
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.rstrip().split()
            lines.append(line[0])
    return lines


PART1_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
PART2_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}
BRACKETS = {"(": ")", "[": "]", "{": "}", "<": ">"}
BRACKETS_REVERSE = {k: v for v, k in BRACKETS.items()}


@timing()
def part1(lines: List[str]) -> int:
    total = 0
    for line in lines:
        stack = []

        for char in line:
            if char in BRACKETS:
                stack.append(char)
            elif char in BRACKETS_REVERSE:
                if stack[-1] != BRACKETS_REVERSE[char]:
                    total += PART1_POINTS[char]
                    break
                else:
                    stack.pop()

    return total


@timing()
def part2(lines: List[str]) -> int:
    scores: List[int] = []
    for line in lines:
        total = 0
        stack: List[str] = []

        for char in line:
            if char in BRACKETS:
                stack.append(char)
            elif char in BRACKETS_REVERSE:
                if stack[-1] != BRACKETS_REVERSE[char]:
                    break
                else:
                    stack.pop()
        else:
            for char in reversed(stack):
                total = (total * 5) + PART2_POINTS[BRACKETS[char]]
            scores.append(total)

    return sorted(scores)[len(scores) // 2]


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    sample = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    check_result(26397, part1(sample))
    check_result(370407, part1(puzzle))

    check_result(288957, part2(sample))
    check_result(3249889609, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
