import re
import sys
from collections import Counter

from support import InputReader, asserter, timing

RE = re.compile(r"(.*)\-(\d+)\[(.*)\]")


@asserter
def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        name, id, checksum = RE.findall(line)[0]
        counts: Counter[str] = Counter(name.replace("-", ""))
        common = sorted(counts.most_common(), key=lambda x: (-x[1], x[0]))
        if checksum == "".join(ch for ch, _ in common[:5]):
            total += int(id)

    return total


@asserter
def part2(lines: list[str]) -> int:
    def rot(ch: str, n: int) -> int:
        return 97 + ((ord(ch) - 97) + n) % 26

    # a-z 97-122
    def decrypt(name: str, room_id: int) -> str:
        return "".join(" " if ch == "-" else chr(rot(ch, room_id)) for ch in name)

    for line in lines:
        name, id, _ = RE.findall(line)[0]
        room_id = int(id)
        if "object" in decrypt(name, room_id):
            return room_id

    raise AssertionError("unreachable")


@timing("day04")
def main() -> int:
    i = InputReader(2016, 4).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(1514)
        assert part1(puzzle)(409147)

    def s2() -> None:
        assert part2(puzzle)(991)

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
