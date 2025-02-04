import json
import sys

from support import InputReader, asserter, timing

type T = dict[str, T] | list[T] | str | int


def parse(v: T, part2: bool) -> int:
    if isinstance(v, int):
        return v
    elif isinstance(v, str):
        return 0
    elif isinstance(v, list):
        return sum(parse(b, part2) for b in v)
    elif isinstance(v, dict):
        if part2 and "red" in v.values():
            return 0
        return sum(parse(b, part2) for b in v.values())
    else:
        raise AssertionError("unreachable")


@asserter
def part1(input: str) -> int:
    return parse(json.loads(input), False)


@asserter
def part2(input: str) -> int:
    return parse(json.loads(input), True)


@timing("day12")
def main() -> int:
    i = InputReader(2015, 12).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1('{"a":{"b":4},"c":-1}')(3)
        assert part1(puzzle)(111754)

    def s2() -> None:
        assert part2('[1,[{"b":{"c":"red","b":{"c":"red","b":2}}}],3]')(4)
        assert part2(puzzle)(65402)

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
