import collections
import sys

from support import InputReader, asserter, timing

# MODULO = 1 << 24  # 16777216
MASK = (1 << 24) - 1


def next_secret(n: int) -> int:
    n = (n ^ n << 6) & MASK
    n ^= n >> 5
    n = (n ^ n << 11) & MASK
    # n = ((n * 64) ^ n) % MODULO
    # n = (math.floor(n / 32) ^ n) % MODULO
    # n = ((n * 2048) % MODULO) ^ n
    return n


@asserter
def part1(lines: list[str]) -> int:
    total = 0
    for secret_n in lines:
        n = int(secret_n)
        for _ in range(2000):
            n = next_secret(n)
        total += n
    return total


@asserter
def part2(lines: list[str]) -> int:
    banana_sequences: collections.defaultdict[tuple[int, ...], int]
    banana_sequences = collections.defaultdict(int)

    for _, secret_n in enumerate(lines):
        num = int(secret_n)

        seen: set[tuple[int, ...]] = set()
        diffs: list[int] = []
        for i in range(2000):
            n = next_secret(num)
            diffs.append((n % 10) - (num % 10))
            num = n

            if i >= 3:
                seq = tuple(diffs)
                diffs.pop(0)
                if seq not in seen:
                    banana_sequences[seq] += num % 10
                    seen.add(seq)

    return max(banana_sequences.values())

    #     for j in range(len(diffs) - 4):
    #         k = (diffs[j], diffs[j + 1], diffs[j + 2], diffs[j + 3])
    #         a, b = banana_sequences[k]
    #         if id not in a:
    #             a.add(id)  # keep one banana per monkey
    #             banana_sequences[k] = (a, b + prices[j + 3])
    #
    # best_seq = max(banana_sequences, key=lambda x: banana_sequences[x][1])
    # return banana_sequences[best_seq][1]


@timing("day22")
def main() -> int:
    i = InputReader(2024, 22).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(37327623)
        assert part1(puzzle)(15303617151)

    def s2() -> None:
        assert part2(["1", "2", "3", "2024"])(23)
        assert part2(puzzle)(1727)

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
