import functools

from support import assert_result, read_file_lines, timing

REV = {"/": "*", "*": "/", "-": "+", "+": "-"}


def operation(op: str, left: int, right: int, reverse: bool = False) -> int:
    if reverse:
        op = REV[op]
    match op:
        case "*":
            return left * right
        case "/":
            return left // right
        case "+":
            return left + right
        case "-":
            return left - right
        case _:
            raise AssertionError("unreachable")


@timing("part1")
def part1(lines: list[str]) -> int:
    parsed: dict[str, int | list[str]] = {}

    for line in lines:
        match line.replace(":", "").split():
            case [monkey, num]:
                parsed[monkey] = int(num)
            case [monkey, *rest]:
                parsed[monkey] = rest

    @functools.lru_cache
    def _resolve(name: str) -> int:
        match parsed[name]:
            case int(val):
                return val
            case [left, op, right]:
                res = operation(op, _resolve(left), _resolve(right))
                return res
        raise AssertionError("unreachable")

    return _resolve("root")


@timing("part2")
def part2(lines: list[str]) -> int:  # noqa C901
    parsed: dict[str, int | list[str]] = {}
    root = None
    for line in lines:
        match line.replace(":", "").split():
            case ["humn", *rest]:
                continue
            case ["root", *rest]:
                root = rest
            case [monkey, num]:
                parsed[monkey] = int(num)
            case [monkey, *rest]:
                parsed[monkey] = rest

    assert root is not None

    @functools.lru_cache
    def _resolve(name: str) -> int:
        match parsed[name]:
            case int(val):
                return val
            case [left, op, right]:
                left_val = _resolve(left)
                root_right = _resolve(right)
                return operation(op, left_val, root_right)
            case _:
                raise AssertionError("unreachable")

    # assume we always need to find left value (const)
    root_right = _resolve(root[2])
    expr = parsed[root[0]]

    while True:
        assert not isinstance(expr, int), expr
        lhs_s, op, rhs_s = expr
        try:
            lhs = _resolve(lhs_s)
        except KeyError:  # variable
            rhs = _resolve(rhs_s)
            root_right = operation(op, root_right, rhs, True)
            try:
                expr = parsed[lhs_s]
            except KeyError:
                # loop should end when on 'humn'
                return root_right
        else:
            match op:
                case "-":
                    root_right -= lhs
                    root_right *= -1
                case "+":
                    root_right -= lhs
                case "*":
                    root_right //= lhs
                case "/":
                    root_right = lhs // root_right
                case _:
                    raise AssertionError("unreachable")
            expr = parsed[rhs_s]


# @timing("part2z3")
# def part2_z3(lines: list[str]) -> int:
#     OPS = {
#         "+": lambda a, b: a + b,
#         "-": lambda a, b: a - b,
#         "/": lambda a, b: a / b,
#         "*": lambda a, b: a * b,
#     }
#     from z3 import Int, Optimize, sat

#     o = Optimize()
#     for line in lines:
#         if line.startswith("humn:"):
#             continue
#         elif line.startswith("root:"):
#             _, a, _, b = line.split()
#             o.add(Int(a) == Int(b))
#         elif len(line.split()) == 4:
#             name, rest = line.split(": ")
#             op1, op, op2 = rest.split()
#             o.add(Int(name) == OPS[op](Int(op1), Int(op2)))
#         else:
#             name, rest = line.split(": ")
#             o.add(Int(name) == int(rest))
#     assert o.check() == sat
#     return o.model()[Int("humn")].as_long()


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/21/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/21/puzzle.input")

    assert_result(152, part1(sample))
    assert_result(155708040358220, part1(puzzle))

    assert_result(301, part2(sample))
    assert_result(3342154812537, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
