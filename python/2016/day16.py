import sys

from support import InputReader, asserter, timing

# https://en.wikipedia.org/wiki/Dragon_curve


def dragon_parity(n: int) -> int:
    """parity of dragon curve of length n"""
    gray = n ^ (n >> 1)
    return (gray ^ (n & gray).bit_count()) & 1


@asserter
def solve(input: str, disc_size: int = 20) -> str:
    data = input.strip()
    length = len(data)
    parity, input_parity = 0, 0

    for i in range(length):
        parity ^= data[i] == "1"
        input_parity ^= parity << (i + 1)
    for i in range(1, length + 1):
        parity ^= data[length - i] != "1"
        input_parity ^= parity << (length + i)

    output: list[str] = []

    #        272  100010000
    #        271  100001111
    #       ~271   11110000
    # 272 & ~271      10000
    chunk_size = disc_size & ~(disc_size - 1)
    prev_parity = 0

    j = chunk_size
    while j <= disc_size:
        dragons = j // (length + 1)
        input_cycles = (j - dragons) // (length * 2)
        input_remainder = (j - dragons) % (length * 2)

        p = dragon_parity(dragons)
        p ^= input_cycles & length
        p ^= input_parity >> input_remainder
        p &= 1

        output.append(str((p ^ prev_parity) ^ 1))

        prev_parity = p
        j += chunk_size

    return "".join(output)


@timing("day16")
def main() -> int:
    i = InputReader(2016, 16).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert solve(example, 20)("01100")
        assert solve(puzzle, 272)("01110011101111011")

    def s2() -> None:
        assert solve(puzzle, 35651584)("11001111011000111")

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
