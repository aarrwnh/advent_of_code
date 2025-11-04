import sys
from typing import NamedTuple

from support import InputReader, asserter, timing

# def convert(dec: int) -> str:
#     return ".".join(tuple(str((dec >> (i * 8)) & 0xFF) for i in (3, 2, 1, 0)))


class Range(NamedTuple):
    start: int
    end: int

    @classmethod
    def n(cls, s: str) -> Range:
        return cls(*map(int, s.split("-")))

    def __lt__(self, other: Range) -> bool:
        return (self.start, self.end) < (other.start, other.end)

    def includes(self, addr: int) -> int:
        return self.start <= addr <= self.end

    def overlaps(self, other: Range) -> bool:
        return max(self.start, other.start) <= min(self.end, other.end)


@asserter
def part1(blocked: list[str]) -> int:
    rules = tuple(Range.n(rule) for rule in blocked)
    addr = 0

    while True:
        for rule in rules:
            if rule.includes(addr):
                addr = rule.end
                break
        else:
            return addr
        addr += 1


@asserter
def part2(blocked: list[str], max_range: int) -> int:
    rules = sorted([Range.n(rule) for rule in blocked], reverse=True)
    b = [rules.pop()]

    while rules:
        r1 = rules.pop()
        r2 = b[-1]

        if r1.overlaps(r2):
            b[-1] = Range(min(r1.start, r2.start), max(r1.end, r2.end))
        else:
            b.append(r1)

    return max_range - sum(r.end - r.start + 1 for r in b)


@timing("day20")
def main() -> int:
    i = InputReader(2016, 20).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(3)
        assert part1(puzzle)(31053880)

    def s2() -> None:
        assert part2(example, 10)(2)
        assert part2(puzzle, 1 << 32)(117)

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
