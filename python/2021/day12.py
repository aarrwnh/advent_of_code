from collections import deque, defaultdict
from typing import Dict, List, Set, Tuple
import os
from support import timing


def read_file(filename: str) -> List[str]:
    path = os.path.dirname(__file__) + "/" + filename
    return [line.rstrip() for line in open(path).readlines()]


@timing()
def compute(lines: List[str], count_one_small_cave: bool = False) -> int:
    edges: Dict[str, Set[str]] = defaultdict(set)

    for line in lines:
        left, right = line.split("-")
        edges[left].add(right)
        edges[right].add(left)

    initial = [(("start",), False)]

    done: Set[Tuple[str, ...]] = set()
    todo: deque[Tuple[Tuple[str, ...], bool]] = deque(initial)

    while todo:
        path, double_small = todo.popleft()
        if path[-1] == "end":
            done.add(path)
            continue

        for choice in edges[path[-1]] - {"start"}:
            if choice.isupper() or choice not in path:
                todo.append(((*path, choice), double_small))
            elif (
                count_one_small_cave
                and double_small is False
                and path.count(choice) == 1
            ):
                todo.append(((*path, choice), True))
    return len(done)


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    sample1 = read_file("sample1.input")
    sample2 = read_file("sample2.input")
    sample3 = read_file("sample3.input")
    puzzle = read_file("puzzle.input")

    check_result(10, compute(sample1))
    check_result(19, compute(sample2))
    check_result(226, compute(sample3))
    check_result(5958, compute(puzzle))

    check_result(36, compute(sample1, True))
    check_result(103, compute(sample2, True))
    check_result(150426, compute(puzzle, True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
