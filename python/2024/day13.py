import sys

from support import InputReader, asserter, timing


class P:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"X={self.x} Y={self.y}"


def parse(input: str, scale: int = 0) -> list[list[P]]:
    groups_s = input.split("\n\n")
    groups: list[list[P]] = []
    for g_s in groups_s:
        a: list[P] = []
        for i, g in enumerate(g_s.strip().split("\n")):
            b = g.split("=" if i == 2 else "+")
            c = P(int(b[1].split(",")[0]), int(b[2]))
            if i == 2:  # prize
                c.x += scale
                c.y += scale
            a.append(c)
        groups.append(a)
    return groups


# def part1(input: str) -> int:
#     total = 0
#     A_COST = 3
#     for group in parse(input):
#         u = math.inf
#         A, B, prize = group
#         for i in range(100):
#             if prize.x % B.x == 0 and prize.y % B.y == 0:
#                 m, n = prize.x // B.x, prize.y // B.y
#                 if m == n:
#                     u = min(u, A_COST * i + m)
#             prize.x -= A.x
#             prize.y -= A.y
#             if prize.x < 0 or prize.y < 0:
#                 break
#         if u < math.inf:
#             total += int(u)
#     return total


def calc(input: str, scale: int = 0) -> int:
    # m = A count | cost 3
    # n = B       | cost 1
    #
    # px = Ax * m + Bx * n
    # py = Ay * m + By * n
    #
    # m = ( px - Bx * n ) / Ax
    # n = ( py - By * n ) / Ay
    #
    # ( px - Bx * n )   ( py - By * n )
    # --------------- = ---------------
    #        Ax                Ay
    #
    #           Ay * ( px - Bx * n ) = Ax * ( py - By * n )
    #  ( Ay * px ) - ( Ay * Bx * n ) = ( Ax * py ) - ( Ax * By * n )
    #  Ax * By * n - ( Ay * Bx * n ) = ( Ax * py ) -   Ay * px
    #
    #        n * (Ax * By - Ay * Bx) = Ax * py - Ay * px
    #
    #       Ax * py - Ay * px
    #  n =  -----------------
    #       Ax * By - Ay * Bx
    #
    total = 0
    for group in parse(input, scale):
        A, B, P = group
        n = (A.x * P.y - A.y * P.x) // (A.x * B.y - A.y * B.x)
        m = (P.x - B.x * n) // A.x

        if (A.x * m + B.x * n, A.y * m + B.y * n) == (P.x, P.y):
            total += 3 * m + n

    return total


@asserter
def part1(input: str) -> int:
    return calc(input)


@asserter
def part2(input: str) -> int:
    return calc(input, 10_000_000_000_000)


@timing("day13")
def main() -> int:
    i = InputReader(2024, 13).raw

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(480)
        assert part1(puzzle)(28262)

    def s2() -> None:
        assert part2(puzzle)(101406661266314)

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
