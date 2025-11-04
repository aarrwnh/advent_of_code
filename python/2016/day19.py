import sys

from support import InputReader, asserter, timing

# https://en.wikipedia.org/wiki/Josephus_problem


@asserter
def part1(elves: int) -> int:
    assert elves > 1
    # b = 1
    # p = 0
    # while b <= elves:
    #     p = (p + 2) % b
    #     b += 1
    # return p + 1
    p = 1 << (elves.bit_length() - 1)
    return (((elves - p) * 2) % elves) + 1


@asserter
def part2(elves: int) -> int:
    assert elves > 1
    # a = []
    # for elf in range(1, 100):
    #     a.append(elf)
    #     elves = collections.deque(a)
    #     while len(elves) > 1:
    #         del elves[len(elves) // 2]
    #         elves.append(elves.popleft())
    #     print(f"{elf} => {elves[0]}")

    p = 1
    while p * 3 < elves:
        p *= 3

    if elves < p * 2:
        p = elves - p
    else:
        # handle next half:
        p = elves - p + (elves - p * 2)

    return p


@timing("day19")
def main() -> int:
    i = InputReader(2016, 19).raw

    example = 5
    puzzle = int(i("puzzle"))

    def s1() -> None:
        assert part1(example)(3)
        assert part1(puzzle)(1816277)

    def s2() -> None:
        assert part2(example)(2)
        assert part2(puzzle)(1410967)

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
