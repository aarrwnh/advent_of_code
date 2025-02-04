import sys
from collections.abc import Generator

from support import asserter, timing


def look_say(number: str) -> str:
    result = ""

    repeat = number[0]
    number = number[1:] + " "
    times = 1

    for actual in number:
        if actual != repeat:
            result += str(times) + repeat
            times = 1
            repeat = actual
        else:
            times += 1

    return result


# def look_say(seed: str) -> str:
#     t = ""
#     i = 0
#     while i < len(seed):
#         b = seed[i]
#         c = seed[i:]
#         i += 1
#         count = 0
#         for p in c:
#             if p == b:
#                 count += 1
#             else:
#                 break

#         t += f"{count}{b}"
#         i += count - 1

#     return t


def look_say_2(n: int, seed: str) -> Generator[str, None, None]:
    if n == 0:
        yield seed
    else:
        for prev in look_say_2(n - 1, seed):
            result = []
            i = 0
            while i < len(prev):
                count = 1
                while i < len(prev) - 1 and prev[i] == prev[i + 1]:
                    count += 1
                    i += 1
                result.append(str(count) + prev[i])
                i += 1
            yield "".join(result)


# def lookandsay(n: str):
#     return "".join(str(len(list(g))) + k for k, g in groupby(n))


# def looksay(look):
#     look = str(look)
#     prev, count, say = look[0], 1, ""
#     for char in look[1:]:
#         if char == prev:
#             count += 1
#             continue
#         say += str(count) + prev
#         prev = char
#         count = 1
#     return say + str(count) + prev


@asserter
def part1(num: str) -> int:
    return len(*look_say_2(40, num))
    # for _ in range(40):
    #     num = lookandsay(num)
    # return len(num)


@asserter
def part2(num: str) -> int:
    return len(*look_say_2(50, num))


@timing("day10")
def main() -> int:
    def s1() -> None:
        assert part1("1")(82350)
        assert part1("3113322113")(329356)

    def s2() -> None:
        assert part2("3113322113")(4666278)

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
