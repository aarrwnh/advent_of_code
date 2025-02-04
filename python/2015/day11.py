import sys

from support import asserter, timing

Password = list[int]

S_A = ord("a")
S_Z = ord("z")
NOT_ALLOWED = {ord("i"), ord("o"), ord("l")}
TRANSLATE = {
    ord("h"): ord("j"),
    ord("n"): ord("p"),
    ord("k"): ord("m"),
    S_Z: S_A,
}


def straight(p: Password) -> bool:
    # abc bcd cde [..]
    return any(p[i] == p[i + 1] - 1 == p[i + 2] - 2 for i in range(len(p) - 2))


def not_contains_letters(p: Password) -> bool:
    return not any(i in p for i in NOT_ALLOWED)


def has_pairs(p: Password) -> bool:
    # n = len(p)
    # s = [False] * n
    # pairs = 0
    # for i in range(n - 1):
    #     j = i + 1
    #     if p[i] == p[j] and not s[i] and not s[j]:
    #         s[j] = True
    #         pairs += 1
    # return pairs >= 2

    found = False
    prev = p[0]
    for n in p[1:]:
        if n == prev:
            if found:
                return True
            else:
                found = True
                prev = -1
        else:
            prev = n
    else:
        return False


def next(p: Password) -> None:
    i = len(p) - 1
    while i >= 0:
        ch = p[i]
        p[i] = TRANSLATE.get(ch, ch + 1)
        if ch != S_Z:
            break
        i -= 1

    # idx = 1
    # p[-idx] += 1
    # while p[-idx] > S_Z:
    #     p[-idx] = S_A
    #     idx += 1
    #     p[-idx] += 1


@asserter
def next_pass(lines: list[str]) -> str:
    checks = [straight, not_contains_letters, has_pairs]

    for line in lines:
        password = [ord(x) for x in line]
        next(password)
        while not all(f(password) for f in checks):
            next(password)
        return "".join(chr(x) for x in password)

    raise AssertionError("unreachable")


@timing("day11")
def main() -> int:
    def s1() -> None:
        assert next_pass(["abcdefgh", "hijklmmn", "abbceffg", "abbcegjk", "ghijklmn"])(
            "abcdffaa"
        )
        assert next_pass(["cqjxjnds"])("cqjxxyzz")

    def s2() -> None:
        assert next_pass(["cqjxxyzz"])("cqkaabcc")

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
