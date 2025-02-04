import sys

from support import InputReader, asserter, timing


class Computer:
    def __init__(self, a: int):
        self.a = 0
        self.registers = {"a": a, "b": 0}
        self.ip = 0

    def b(self) -> int:
        return self.registers["b"]

    def parse(self, input: list[str]) -> "Computer":
        self.program = [line.replace(",", "").split() for line in input]
        return self

    def run(self) -> "Computer":
        assert self.program
        while self.ip < len(self.program):
            self._step()
        return self

    def _step(self) -> None:
        offset = 1
        match self.program[self.ip]:
            case "hlf", r:
                self.registers[r] //= 2
            case "tpl", r:
                self.registers[r] *= 3
            case "inc", r:
                self.registers[r] += 1
            case ("jmp", o) if o.startswith("-") or o.startswith("+"):
                offset = int(o)
            case ("jie", r, o) if self.registers[r] % 2 == 0:
                offset = int(o)
            case ("jio", r, o) if self.registers[r] == 1:
                offset = int(o)
        self.ip += offset


@asserter
def part1(lines: list[str]) -> int:
    return Computer(a=0).parse(lines).run().b()


@asserter
def part2(lines: list[str]) -> int:
    return Computer(a=1).parse(lines).run().b()


@timing("day23")
def main() -> int:
    i = InputReader(2015, 23).lines

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(170)

    def s2() -> None:
        assert part2(puzzle)(247)

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
