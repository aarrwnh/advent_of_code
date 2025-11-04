# pyright: basic
import sys
from _md5 import md5  # pyright: ignore[reportMissingImports]
from functools import cache

from support import asserter, timing


def to_hex(input: str, repeat: int = 0) -> str:
    hex = input
    for _ in range(repeat + 1):
        hex = md5(hex.encode()).hexdigest()
    return hex


@cache
def parse_salt(salt: str, repeat: int = 0) -> tuple[str, None | str, None | str]:
    hex = to_hex(salt, repeat)
    triplet = None
    quintuple = None
    size = len(hex) + 1
    for j in range(size - 3):
        if len(set(hex[j:j + 3])) == 1:
            triplet = hex[j]
            for i in range(j, size - 5):
                if len(set(hex[i:i + 5])) == 1:
                    quintuple = hex[i]
                    break
            break
    return hex, triplet, quintuple


def find_key(salt: str, *, stretch_amount: int = 0) -> int:
    i, f = 0, 0
    while f < 64:
        _, triplet, _ = parse_salt(f"{salt}{i}", stretch_amount)
        i += 1
        if triplet is None:
            continue
        for p in range(i, i + 1000):
            _, _, quintuple = parse_salt(f"{salt}{p}", stretch_amount)
            if quintuple is None:
                continue
            if triplet == quintuple:
                f += 1
                break
    return i - 1


@asserter
def part1(salt: str) -> int:
    return find_key(salt)


@asserter
def part2(salt: str) -> int:
    return find_key(salt, stretch_amount=2016)


@timing("day14")
def main() -> int:
    example = "abc"
    puzzle = "ahsbgdzn"

    def s1() -> None:
        assert part1(example)(22728)
        assert part1(puzzle)(23890)

    def s2() -> None:
        assert part2(example)(22551)
        assert part2(puzzle)(22696)

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
