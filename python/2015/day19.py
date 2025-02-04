import sys
from collections.abc import Generator

from support import InputReader, asserter, timing


def split(s: str, line: str) -> Generator[str]:
    src, dest = line.split(" => ")
    parts = s.split(src)
    for i in range(1, len(parts)):
        yield src.join(parts[:i]) + dest + src.join(parts[i:])


@asserter
def part1(input: str) -> int:
    r_s, molecule = input.rstrip().split("\n\n")
    found = set()
    for line in r_s.splitlines():
        found.update(split(molecule, line))
    return len(found)


@asserter
def part2(input: str) -> int:
    r_s, molecule = input.rstrip().split("\n\n")

    r: list[tuple[str, str]] = []
    for line in r_s.splitlines():
        lhs, rhs = line.split(" => ")
        r.append((lhs, rhs))

    # try from longest first
    r.sort(key=lambda kv: -len(kv[1]))

    step = 0
    while molecule != "e":
        for src, dest in r:
            p = molecule.find(dest)
            while p > -1:
                step += 1
                molecule = molecule[:p] + src + molecule[p + len(dest) :]
                p = molecule.find(dest, p + 1)
    return step


@timing("day19")
def main() -> int:
    i = InputReader(2015, 19).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(4)
        assert part1(puzzle)(518)

    def s2() -> None:
        assert part2(example)(3)
        assert part2(puzzle)(200)

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
