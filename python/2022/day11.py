from typing import Callable

from support import check_result, read_file_raw, timing  # type: ignore


def add(rhs: int):
    def f(lhs: int) -> int:
        return rhs + lhs

    return f


def multi(rhs: int):
    def f(lhs: int) -> int:
        return lhs * rhs

    return f


def square():
    def f(lhs: int) -> int:
        return lhs * lhs

    return f


def parse(
    input: str,
) -> list[tuple[list[int], int, Callable[[int], int], int, int]]:
    out = []
    for _, m in enumerate(input.split("\n\n")):
        _, items_s, op_s, test_s, t_s, f_s = m.splitlines()
        items = [int(x.replace(",", "")) for x in items_s.split(" ")[4:]]
        test = int(test_s.split(" ")[-1])
        op_s = op_s.split(": ")[-1].split(" = ")[1]

        if op_s == "old * old":
            fn = square()
        elif " * " in op_s:
            fn = multi(int(op_s.split()[-1]))
        elif " + " in op_s:
            fn = add(int(op_s.split()[-1]))
        else:
            raise AssertionError("!")

        next_true = int(t_s.split(" ")[-1])
        next_false = int(f_s.split(" ")[-1])
        out.append((items, test, fn, next_true, next_false))
    return out


@timing()
def part1(input: str) -> int:
    monkeys = parse(input)
    count = [0] * len(monkeys)
    for r in range(20):
        for idx, m in enumerate(monkeys):
            items, test, operation, t, f = m
            for item in items:
                new = operation(item) // 3
                count[idx] += 1
                monkeys[t if new % test == 0 else f][0].append(new)

            items.clear()

    a = sorted(count)
    return a[-1] * a[-2]


@timing()
def part2(input: str) -> int:
    monkeys = parse(input)
    count = [0] * len(monkeys)

    # https://en.wikipedia.org/wiki/Modular_arithmetic
    # (x % y) % z == (x % z) if y % z == 0

    # keep track of all separately ?
    modulus = 1
    for m in monkeys:
        modulus *= m[1]

    for r in range(10000):
        for idx, m in enumerate(monkeys):
            items, test, operation, t, f = m
            for item in items:
                new = operation(item) % modulus
                count[idx] += 1
                target = t if new % test == 0 else f
                monkeys[target][0].append(new)

            items.clear()

    a = sorted(count)
    return a[-1] * a[-2]


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/11/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/11/puzzle.input")

    check_result(10605, part1(sample))
    check_result(61503, part1(puzzle))

    check_result(2713310158, part2(sample))
    check_result(14081365540, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
