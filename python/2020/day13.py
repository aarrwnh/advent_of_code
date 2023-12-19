import math
import sys

from support import InputReader, asserter, timing


@asserter
@timing("part1")
def part1(input: str) -> int:
    time_s, ids_s = input.splitlines()
    time = int(time_s)
    d: dict[int, int] = {}
    for id_s in ids_s.split(","):
        if id_s == "x":
            continue
        id = int(id_s)
        d[id] = id - time % id
    a = min(d.items(), key=lambda x: x[1])
    return math.prod(a)


@asserter
@timing("part2")
def part2(input: str) -> int:
    _, ids_s = input.splitlines()
    d = [(int(s), i) for i, s in enumerate(ids_s.split(",")) if s != "x"]

    mult = d[0][0]
    t = 0

    # Chinese Remainder Theorem
    # t + column modulo bus_id = 0
    # t % 7 == 0
    # t % 13 == 12 | (t+1) % 13 == 0)
    # t % 59 == 55 | (t+4)

    for bus_id, offset in d[1:]:
        while (t + offset) % bus_id != 0:
            t += mult
        mult *= bus_id

    return t


def main() -> int:
    i = InputReader(2020, 13).raw

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(295)
        assert part1(puzzle)(2382)

    def s2() -> None:
        assert part2("\n17,x,13,19")(3417)
        assert part2("\n67,7,59,61")(754018)
        assert part2("\n67,x,7,59,61")(779210)
        assert part2("\n67,7,x,59,61")(1261476)
        assert part2("\n1789,37,47,1889")(1202161486)
        assert part2(sample)(1068781)
        assert part2(puzzle)(906332393333683)

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
