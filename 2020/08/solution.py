from typing import List
import os


def read_file(path: str) -> List[List[str]]:
    lines: List[List[str]] = []
    with open(path, "r") as f:
        for line in f.readlines():
            lines.append([*line.rstrip().split("\x20")])
    return lines


sample = list(
    map(
        lambda x: x.split("\x20"),
        """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip().split(
            "\n"
        ),
    )
)


def part1(arr: List[List[str]], part1: bool = True) -> int:
    idx: int = 0
    acc: int = 0
    visited: List[int] = []
    while True:
        if idx >= len(arr):
            return acc
        if idx in visited:
            return acc if part1 else False
        visited.append(idx)
        method, value = arr[idx]
        value = int(value)

        if method == "nop":
            idx += 1
        elif method == "jmp":
            idx += value
        elif method == "acc":
            idx += 1
            acc += value
    return acc


def part2(lines: List[List[str]]):
    for idx, line in enumerate(lines):
        method = line[0]
        if method == "nop" or line[0] == "jmp":
            prev = method
            lines[idx][0] = "nop" if method == "jmp" else "jmp"
            if accumulator := part1(lines, False):
                return accumulator
            lines[idx][0] = prev


def main() -> int:
    lines = read_file(os.path.dirname(__file__) + "/puzzle.input")

    print(part1(sample), 5)
    print(part2(sample), 8)

    print(part1(lines), 1832)
    print(part2(lines), 662)

    return 0


if __name__ == "__main__":
    main()
