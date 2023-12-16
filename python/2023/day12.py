import sys
from functools import lru_cache

from support import InputReader, asserter, timing


def unfold(input: str, separator: str, times: int = 5) -> str:
    return separator.join([input] * times)


def size_to_tuple(input: str) -> tuple[int, ...]:
    return tuple(int(elem) for elem in input.split(","))


@lru_cache(maxsize=1024)
def count_hash(pattern: tuple[str, ...], group_sizes: tuple[int, ...]) -> int:
    n = group_sizes[0]
    if len(pattern) < n or "." in pattern[0:n]:
        # enough springs for the group
        return 0
    if len(pattern) == n:
        if len(group_sizes) == 1:
            # valid : everything matched
            return 1
        else:
            return 0
    if pattern[n] == "#":
        return 0
    return count_possible(pattern[n + 1 :], group_sizes[1:])


@lru_cache(maxsize=1024)
def count_possible(pattern: tuple[str, ...], group_sizes: tuple[int, ...]) -> int:
    if len(group_sizes) == 0:
        if "#" not in pattern:
            # valid : no groups and have no springs left then the rest of ? can be .
            return 1
        else:
            # invalid : there are springs to match but no groups left
            return 0

    remaining = sum(group_sizes) + len(group_sizes) - 1
    if len(pattern) < remaining:
        # invalid : not enough springs left to fit group/s
        return 0

    match pattern[0]:
        case ".":
            return count_possible(pattern[1:], group_sizes)
        case "#":
            return count_hash(pattern, group_sizes)
        case "?":
            a = count_possible(pattern[1:], group_sizes)
            b = count_hash(pattern, group_sizes)
            return a + b
        case _:
            raise AssertionError("unreachable")


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        pattern, groups = line.split(" ")
        b = size_to_tuple(groups)
        total += count_possible(tuple(pattern), b)
    return total


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        pattern, groups = line.split(" ")
        b = size_to_tuple(unfold(groups, ",", 5))
        total += count_possible(tuple(unfold(pattern, "?", 5)), b)
    return total


@timing("main")
def main() -> int:
    i = InputReader(2023, 12)

    sample = i.lines("sample")
    puzzle = i.lines("puzzle")

    def s1() -> None:
        part1(sample)(21)
        part1(puzzle)(7670)

    def s2() -> None:
        part2(sample)(525152)
        part2(puzzle)(157383940585037)

        print(count_hash.cache_info())
        print(count_possible.cache_info())

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


# part 1 brute
# def gen(s: str) -> Generator[str, None, None]:
#     if not s:
#         yield ""
#         return
#     for rest in gen(s[1:]):
#         if s[0] == "?":
#             yield "." + rest
#             yield "#" + rest
#         else:
#             yield s[0] + rest
# def counts(s: str) -> list[int]:
#     s = re.sub(r"\.+", ".", s.strip("."))
#     return [len(s) for s in s.split(".")]
