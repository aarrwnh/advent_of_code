import collections
import re
import sys
from collections.abc import Iterator

from support import InputReader, asserter, timing


def step_to_hash(input: str) -> int:
    v = 0
    for ch in input:
        v = ((v + ord(ch)) * 17) % 256
    return v


@asserter
@timing("part1")
def part1(input: str) -> int:
    return sum(step_to_hash(step) for step in input.strip().split(","))


_Boxes = collections.defaultdict[int, list[tuple[str, int]]]


@asserter
@timing("part2")
def part2(input: str) -> int:
    boxes: _Boxes = collections.defaultdict(list)

    def f(stp: str, idx: int) -> Iterator[tuple[str, int]]:
        return filter(lambda x: x[0] == stp, boxes[idx])

    for s in input.strip().split(","):
        step, sep, b_s = re.split(r"([-=])", s, maxsplit=1)
        focal_len = int(b_s) if b_s else 0
        idx = step_to_hash(step)
        match sep:
            case "-":
                for slot in f(step, idx):
                    boxes[idx].remove(slot)
                    break
                    # if len(boxes[idx]) == 0:
                    #     boxes.pop(idx)
            case "=":
                for slot in f(step, idx):
                    j = boxes[idx].index(slot)
                    boxes[idx][j] = (step, focal_len)
                    break
                else:
                    boxes[idx].append((step, focal_len))

    return focusing_power(boxes)


def focusing_power(boxes: _Boxes) -> int:
    total = 0
    for box_id, box in boxes.items():
        for slot, (_, focal_len) in enumerate(box, 1):
            total += (1 + box_id) * slot * focal_len
    return total


def main() -> int:
    i = InputReader(2023, 15).raw

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(1320)
        assert part1(puzzle)(503487)

    def s2() -> None:
        assert part2(sample)(145)
        assert part2(puzzle)(261505)

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
