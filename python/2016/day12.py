from __future__ import annotations

import sys

from support import InputReader, asserter, timing

Value = int | str


class Machine:
    ip: int = 0
    instructions: list[tuple[Value, ...]] = []
    prev_seq: list[tuple[Value, ...]] = []

    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0

    def __init__(self, instructions: list[str], *, c: int = 0):
        self.c = c
        self.instructions = [
            tuple(
                int(y) if y.isnumeric() or y.startswith("-") else y
                for y in x.split(" ")
            )
            for x in instructions
        ]

    def get_reg(self, x: Value) -> int:
        if isinstance(x, int):
            return x
        assert hasattr(self, x)
        return getattr(self, x)

    def set_reg(self, x: Value, y: int):
        assert hasattr(self, str(x))
        setattr(self, str(x), y)

    def run(self) -> Machine:
        while self.ip < len(self.instructions):
            self.step()
        return self

    def step(self):
        offset = 1
        self.prev_seq.append(self.instructions[self.ip])
        match self.instructions[self.ip]:
            case "cpy", x, y:
                self.set_reg(y, self.get_reg(x))
            case "inc", x:
                self.set_reg(x, self.get_reg(x) + 1)
            case "dec", x:
                self.set_reg(x, self.get_reg(x) - 1)
            case "jnz", x, y:
                if self.get_reg(x) != 0:
                    key = tuple(self.prev_seq)

                    if len(key) in {3, 4} and key[-3][0] == "inc" and int(key[-1][2]) < 0:
                        # and not any(False for x in key if x[0] == "cpy"):
                        #
                        # do loopin math
                        #  (('inc', 'a'), ('dec', 'b'), ('jnz', 'b', -2)): 317760,
                        #  (('inc', 'a'), ('dec', 'd'), ('jnz', 'd', -2)): 156,
                        #  (('cpy', 14, 'd'), ('inc', 'a'), ('dec', 'd'), ('jnz', 'd', -2)): 12,
                        #  (('cpy', 'a', 'c'), ('inc', 'a'), ('dec', 'b'), ('jnz', 'b', -2)): 24,
                        a = {t[0]: t[1] for t in key}
                        dec = a["dec"]
                        inc = a["inc"]
                        b = self.get_reg(dec)
                        self.set_reg(dec, 0)
                        self.set_reg(inc, self.get_reg(inc) + b)
                    else:
                        offset = int(y)

                    self.prev_seq.clear()
            case _:
                raise AssertionError("unreachable")
        self.ip += offset


@asserter
def part1(lines: list[str]) -> int:
    return Machine(lines).run().get_reg("a")


@asserter
def part2(lines: list[str]) -> int:
    return Machine(lines, c=1).run().get_reg("a")


@timing("day12")
def main() -> int:
    i = InputReader(2016, 12).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(42)
        assert part1(puzzle)(317993)

    def s2() -> None:
        assert part2(puzzle)(9227647)

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
