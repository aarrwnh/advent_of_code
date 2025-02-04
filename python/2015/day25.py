from support import InputReader, asserter, timing


@asserter
def part1(input: str) -> int:
    row, col = tuple(int(x.split()[-1].rstrip(".")) for x in input.split(",")[1:])

    p = 20151125
    mod = 33554393
    result = p % mod
    base = 252533 % mod
    exp = (1 + (col + row - 1) * (col + row) // 2 - row) - 1

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod

    return result

    # i = 2
    # while True:
    #     x = 1
    #     y = i
    #     for j in range(i):
    #         p = (p * 252533) % mod
    #         if x + j == col and y - j == row:
    #             return p
    #     i += 1


@timing("day25")
def main() -> int:
    i = InputReader(2015, 25).raw

    puzzle = i("puzzle")

    assert part1(puzzle)(19980801)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
