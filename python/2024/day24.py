import operator
import sys
from collections.abc import Callable

from support import InputReader, asserter, timing

OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}


Wires = dict[str, int]
Gates = list["Gate"]


class Gate:
    def __init__(self, A: str, B: str, operator: str, output: str):
        self.A = A
        self.B = B
        self.operator = operator
        self.op: Callable[[int, int], int]
        self.op = OPS[operator]
        self.output = output

    def check(self, wires: Wires) -> bool:
        if self.A not in wires or self.B not in wires:
            return False
        wires[self.output] = self.op(wires[self.A], wires[self.B])
        return True

    # def __repr__(self):
    #     return f"{self.A} {self.operator} {self.B} -> {self.output}"


def parse(input: str) -> tuple[Wires, Gates]:
    v_s, g_s = input.split("\n\n")
    wires: Wires = {}
    gates: Gates = []
    for line in v_s.splitlines():
        k, v = line.split(": ")
        wires[k] = int(v)
    for line in g_s.splitlines():
        left, op, right, _, name = line.split(" ")
        gates.append(Gate(left, right, op, name))
    return wires, gates


def resolve(wires: Wires, gates: Gates) -> Gates:
    next: Gates = []
    for gate in gates:
        if not gate.check(wires):
            next.append(gate)
    return next


@asserter
def part1(input: str) -> int:
    wires, gates = parse(input)

    while len(gates) > 0:
        gates = resolve(wires, gates)

    return combine_output(wires)


def fill_wires(x: int, y: int) -> Wires:
    wires: Wires = {}
    for k in range(45):
        wires[f"x{k:02}"] = 1 if (x >> k) & 1 == 1 else 0
        wires[f"y{k:02}"] = 1 if (y >> k) & 1 == 1 else 0
    return wires


def check_bit_sequence(gates: Gates, num: int) -> bool:
    for a in [1, 3]:
        for b in [1, 3]:
            x = a << max(num - 1, 0)
            y = b << max(num - 1, 0)
            wires = fill_wires(x, y)

            prev_gates: Gates = []
            gates0 = gates
            while len(gates0) > 0:
                gates0 = resolve(wires, gates0)

                if len(prev_gates) == len(gates0):
                    return False

                prev_gates = gates0

            if x + y != combine_output(wires):
                return False

            wires.clear()

    return True


def find_gates_1(gates: Gates, a: str) -> list[int]:
    res = []
    for i, g in enumerate(gates):
        if a == g.A or a == g.B:
            res.append(i)
    return res


def find_gates_2(gates: Gates, a: str, b: str) -> list[int]:
    res = []
    for i, g in enumerate(gates):
        if (a == g.A and b == g.B) or (b == g.A and a == g.B):
            res.append(i)
    return res


def extract_adder(gates: Gates, n: int) -> list[int]:
    adder: list[int] = []

    adder.extend(find_gates_1(gates, f"x{n:02}"))
    adder.extend(find_gates_1(gates, gates[adder[0]].output))
    adder.extend(find_gates_1(gates, gates[adder[1]].output))

    for i, a in enumerate(adder):
        ac = gates[a].output
        for b in adder[i + 1 :]:
            bc = gates[b].output
            res = find_gates_2(gates, ac, bc)
            if len(res) > 0:
                adder.extend(res)
                return adder

    return adder


def swap(gates: Gates, a: int, b: int) -> None:
    gates[a].output, gates[b].output = gates[b].output, gates[a].output


def test_outputs(gates: Gates, adder: list[int], n: int) -> list[str]:
    for i, a in enumerate(adder):
        for b in adder[i + 1 :]:
            swap(gates, a, b)
            if check_bit_sequence(gates, n):
                return [gates[a].output, gates[b].output]
            # swap back if didn't find bad bits
            swap(gates, a, b)
    return []


@asserter
def part2(input: str) -> str:
    _, gates = parse(input)

    swapped_pairs: list[str] = []
    for n in range(45):
        if not check_bit_sequence(gates, n):
            adder = extract_adder(gates, n)
            swapped = test_outputs(gates, adder, n)
            swapped_pairs.extend(swapped)

    swapped_pairs.sort()
    return ",".join(swapped_pairs)


def combine_output(wires: Wires) -> int:
    num = 0
    for i in range(64):
        if wires.get(f"z{i:02}", 0) == 1:
            num |= 1 << i
    return num


@timing("day24")
def main() -> int:
    i = InputReader(2024, 24).raw

    example1 = i("example-1")
    # example2 = i("example-2")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example1)(2024)
        assert part1(puzzle)(60714423975686)

    def s2() -> None:
        assert part2(puzzle)("cgh,frt,pmd,sps,tst,z05,z11,z23")

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


# def part1(input: str) -> int:
#     v_s, g_s = input.split("\n\n")
#     wires: dict[str, int] = {}
#     gates: dict[str, list[str]] = {}
#     for line in v_s.splitlines():
#         k, v = line.split(": ")
#         wires[k] = int(v)
#     for line in g_s.splitlines():
#         left, op, right, _, name = line.split(" ")
#         gates[name] = [left, op, right]

#     @cache
#     def resolve(gate_name: str) -> int:
#         if gate_name in wires:
#             return wires[gate_name]

#         left, op, right = gates[gate_name]
#         match op:
#             case "AND":
#                 return resolve(left) & resolve(right)
#             case "OR":
#                 return resolve(left) | resolve(right)
#             case "XOR":
#                 return resolve(left) ^ resolve(right)
#         raise AssertionError("unreachable")

#     for name in gates:
#         wires[name] = resolve(name)

#     return combine_output(wires)
