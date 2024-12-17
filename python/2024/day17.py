import re
import sys

from support import InputReader, asserter, timing


class Computer:
    def __init__(self, A: int, B: int, C: int, program: list[int]) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.ip = 0
        self.program = program

    def reset(self, A: int) -> "Computer":
        assert A is not None
        self.A = A
        self.B = 0
        self.C = 0
        self.ip = 0
        return self

    def run(self) -> list[int]:
        output: list[int] = []
        while self.ip < len(self.program):
            res = self._step()
            if res is not None:
                output.append(res)
        return output

    def _step(self) -> None | int:
        opcode = self.program[self.ip]
        literal = self.program[self.ip + 1]
        self.ip += 2
        return self._instruction(opcode, literal)

    def _instruction(self, opcode: int, literal: int) -> None | int:
        result = None
        combo = self._combo_value(literal)
        match opcode:
            case 0:  # adv
                self.A = self.A >> combo
            case 1:  # bxl
                self.B = self.B ^ literal
            case 2:
                self.B = combo % 8
            case 3:
                if self.A != 0:
                    self.ip = literal
            case 4:
                self.B = self.B ^ self.C
            case 5:  # out
                result = combo % 8
            case 6:
                self.B = self.A >> combo
            case 7:
                self.C = self.A >> combo

        return result

    def _combo_value(self, literal: int) -> int:
        match literal:
            case 0 | 1 | 2 | 3:
                return literal
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise AssertionError("7 is reserved")
        raise AssertionError("wrong combo operand")


def parse(input: str) -> tuple[list[int], ...]:
    r_s, p_s = input.split("\n\n")
    registers = [int(x) for x in re.findall("\\d+", r_s)]
    program = [int(x) for x in re.findall("\\d+", p_s)]
    return registers, program


@asserter
def part1(input: str) -> str:
    [A, B, C], prog = parse(input)
    result = Computer(A, B, C, prog).run()
    return ",".join(str(x) for x in result)


@asserter
def part2(input: str) -> int:
    [A, B, C], prog = parse(input)

    # b = a % 8
    # b = b ^ 7
    # c = a >> b
    # b = b ^ 7
    # a = a >> 3
    # b = b ^ c
    # output b % 8
    # goto 0

    dev = Computer(A, B, C, prog)

    candidates: list[int] = []
    for a in range(1, 3 << 8): # 704
        output = dev.reset(a).run()
        if output[0] == dev.program[0]:
            candidates.append(a)

    pos = 1
    while pos < len(dev.program):
        n: list[int] = []

        for canditate in candidates:
            for bit in range(0, 8):
                num = (bit << (7 + 3 * pos)) | canditate
                output = dev.reset(num).run()
                if len(output) > pos and output[pos] == dev.program[pos]:
                    n.append(num)
        pos += 1
        candidates = n

    return min(candidates)


@timing("day17")
def main() -> int:
    i = InputReader(2024, 17).raw

    example1 = i("example-1")
    example2 = i("example-2")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example1)("4,6,3,5,6,3,5,2,1,0")
        assert part1(puzzle)("7,3,5,7,5,7,4,3,0")

    def s2() -> None:
        assert part2(example2)(117440)
        assert part2(puzzle)(105734774294938)

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
