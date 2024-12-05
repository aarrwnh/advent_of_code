import sys
from collections import defaultdict

from support import InputReader, asserter, timing


@asserter
@timing("part1")
def part1(input: str) -> int:
    ordering_s, numbers_s = input.split("\n\n")
    lst = [[int(x) for x in n.split(",")] for n in numbers_s.split()]
    ordering = [tuple(int(x) for x in line.split("|")) for line in ordering_s.split()]

    def u(num: list[int]) -> int:
        for i, a in enumerate(num):
            for b in num[i + 1 :]:
                if (a, b) not in ordering:
                    return 0
        return int(num[len(num) // 2])

    return sum(u(num) for num in lst)


@asserter
@timing("part2")
def part2(input: str) -> int:
    total = 0

    ordering_s, numbers_s = input.split("\n\n")
    lst = [[int(x) for x in n.split(",")] for n in numbers_s.split()]

    edges = defaultdict(set)
    for line in ordering_s.split():
        x_s, y_s = line.split("|")
        edges[int(x_s)].add(int(y_s))

    def sortme(num: list[int]) -> list[int]:
        indices: defaultdict[int, int] = defaultdict(int)
        for i, a in enumerate(num):
            for b in num[i + 1 :]:
                if a in edges[b]:
                    indices[a] += 1
                if b in edges[a]:
                    indices[b] += 1

        todo = []
        stack = []

        for a in num:
            if indices[a] == 0:
                todo.append(a)
                stack.append(a)

        while todo:
            a = todo.pop(0)
            for b in edges[a]:
                indices[b] -= 1
                if indices[b] == 0:
                    todo.append(b)
                    stack.append(b)

        return stack

    def u(n: list[int], i: int, a: int) -> int:
        for b in n[i + 1 :]:
            if a in edges[b]:
                new_n = sortme(n)
                return int(new_n[len(new_n) // 2])
        return 0

    for n in lst:
        for i, a in enumerate(n):
            if (v := u(n, i, a)) != 0:
                total += v
                break

    return total


def main() -> int:
    i = InputReader(2024, 5).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(143)
        assert part1(puzzle)(5166)

    def s2() -> None:
        assert part2(example)(123)
        assert part2(puzzle)(4679)

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
