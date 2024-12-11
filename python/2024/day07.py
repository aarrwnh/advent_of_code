import math
import sys
from collections.abc import Generator
from typing import NamedTuple

from support import InputReader, asserter, timing


class Calibaration(NamedTuple):
    test_value: int
    numbers: tuple[int, ...]
    size: int

    def get(self, idx: int) -> int:
        return self.numbers[idx]

    def _eval(self, ops: tuple[str, ...], value: int, idx: int) -> bool:
        if idx >= self.size:
            return value == self.test_value
        for op in ops:
            n_value = operation(op, value, self.get(idx))
            if n_value > self.test_value:
                continue
            if self._eval(ops, n_value, idx + 1):
                return True
        return False

    def reverse_eval(self, concat: bool = False) -> bool:
        def is_valid(value: int, nums: list[int]) -> int:
            if value % 1 > 0 or not nums:
                return 0
            *nums, tail = nums

            if (
                (value == tail and not nums)
                or is_valid(operation("/", value, tail), nums)
                or is_valid(operation("-", value, tail), nums)
                or (concat and is_valid(operation("|", value, tail), nums))
            ):
                return value
            return 0

        return is_valid(self.test_value, [*self.numbers]) != 0


# def eval_brute(ops: tuple[str, ...], test_value: int, nums: tuple[int, ...]) -> int:
#     for a in itertools.product(ops, repeat=len(nums) - 1):
#         value = nums[0]
#         for i, op in enumerate(a):
#             value = operation(op, value, nums[i + 1])
#             if value > test_value:
#                 break
#         if value == test_value:
#             return True
#     return False


def parse(lines: list[str]) -> Generator[Calibaration, None, None]:
    for line in lines:
        left_s, right_s = line.split(": ")
        numbers = tuple(int(r) for r in right_s.split(" "))
        yield Calibaration(int(left_s), numbers, len(numbers))


def operation(op: str, a: int, b: int) -> int:
    match op:
        case "/":
            return a / b  # type: ignore
        case "-":
            return a - b
        case "*":
            return a * b
        case "+":
            return a + b
        case "||":
            f = 10 ** (math.floor(math.log10(b)) + 1)
            return a * f + b
        case "|":
            f = 10 ** (math.floor(math.log10(b)) + 1)
            return (a - b) / f
        case _:
            raise AssertionError("unreachable")


@asserter
def part1(lines: list[str]) -> int:
    # ops = ("+", "*")
    return sum(c.test_value for c in parse(lines) if c.reverse_eval())


@asserter
def part2(lines: list[str]) -> int:
    # ops = ("+", "*", "||")
    return sum(c.test_value for c in parse(lines) if c.reverse_eval(concat=True))


def main() -> int:
    i = InputReader(2024, 7).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(3749)
        assert part1(puzzle)(1153997401072)

    def s2() -> None:
        assert part2(example)(11387)
        assert part2(puzzle)(97902809384118)

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
