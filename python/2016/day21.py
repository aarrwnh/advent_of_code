import sys

from support import InputReader, asserter, timing

Password = list[str]


class Instruction:
    def action(self, _pswd: Password) -> Password: ...

    def reverse(self, pswd: Password) -> Password:
        return self.action(pswd)

    @staticmethod
    def _swap(pswd: Password, src: int, dest: int) -> Password:
        pswd[src], pswd[dest] = pswd[dest], pswd[src]
        return pswd

    @staticmethod
    def _rotate(pswd: Password, step: int) -> Password:
        return pswd[step:] + pswd[:step]


class SwapPosition(Instruction):
    src: int
    dest: int

    def __init__(self, src: str, dest: str):
        self.src = int(src)
        self.dest = int(dest)

    def action(self, pswd: Password) -> Password:
        return self._swap(pswd, self.src, self.dest)


class SwapLetter(Instruction):
    char1: str
    char2: str

    def __init__(self, char1: str, char2: str):
        self.char1 = char1
        self.char2 = char2

    def action(self, pswd: Password) -> Password:
        src = pswd.index(self.char1) if self.char1 in pswd else None
        dest = pswd.index(self.char2) if self.char2 in pswd else None
        assert src is not None and dest is not None
        return self._swap(pswd, src, dest)


class ReversePosition(Instruction):
    src: int
    dest: int

    def __init__(self, src: str, dest: str):
        self.src = int(src)
        self.dest = int(dest)

    def action(self, pswd: Password) -> Password:
        for x, char in enumerate(pswd[self.src : self.dest + 1]):
            pswd[self.dest - x] = char
        return pswd


class Rotate(Instruction):
    n: int

    def __init__(self, dir: str, src: str):
        self.n = -int(src) if dir == "left" else int(src)

    def action(self, pswd: Password) -> Password:
        return self._rotate(pswd, -self.n)

    def reverse(self, pswd: Password) -> Password:
        return self._rotate(pswd, self.n)


class MovePosition(Instruction):
    src: int
    dest: int

    def __init__(self, src: str, dest: str):
        self.src = int(src)
        self.dest = int(dest)

    @staticmethod
    def _action(pswd: Password, src: int, dest: int) -> Password:
        temp = pswd[src]
        del pswd[src]
        pswd.insert(dest, temp)
        return pswd

    def action(self, pswd: Password) -> Password:
        return self._action(pswd, self.src, self.dest)

    def reverse(self, pswd: Password) -> Password:
        return self._action(pswd, self.dest, self.src)


class RotateBased(Instruction):
    char: str

    def __init__(self, char: str):
        self.char = char

    def action(self, pswd: Password) -> Password:
        idx = pswd.index(self.char)
        n = 1 + idx + (idx >= 4)
        return self._rotate(pswd, -n % len(pswd))

    def reverse(self, pswd: Password) -> Password:
        p = pswd
        while True:
            p = self._rotate(p, 1)
            if self.action(p) == pswd:
                break
        return p


def parse_instructions(instructions: list[str]) -> list[Instruction]:
    v: list[Instruction] = []
    for inst in instructions:
        match inst.split(" "):
            case ("swap", "position", src, _, _, dest):
                v.append(SwapPosition(src, dest))
            case ("swap", "letter", char1, _, _, char2):
                v.append(SwapLetter(char1, char2))
            case ("reverse", "positions", src, _, dest):
                v.append(ReversePosition(src, dest))
            case ("rotate", dir, src, ("step" | "steps")):
                v.append(Rotate(dir, src))
            case ("move", "position", src, _, _, dest):
                v.append(MovePosition(src, dest))
            case ("rotate", "based", _, "position", _, "letter", char):
                v.append(RotateBased(char))
            case _:
                raise NotImplementedError
    return v


def scrambler(
    password: str, instructions: list[Instruction], reverse: bool = False
) -> str:
    pswd = list(password)
    if reverse:
        instructions = list(reversed(instructions))

    for inst in instructions:
        match inst:
            case (
                SwapPosition()
                | SwapLetter()
                | ReversePosition()
                | Rotate()
                | MovePosition()
                | RotateBased()
            ):
                pswd = inst.reverse(pswd) if reverse else inst.action(pswd)
            case _:
                raise NotImplementedError

    return "".join(pswd)


@asserter
def part1(password: str, instructions: list[str]) -> str:
    return scrambler(password, parse_instructions(instructions))


@asserter
def part2(scrambled_password: str, instructions: list[str]) -> str:
    return scrambler(
        scrambled_password,
        parse_instructions(instructions),
        reverse=True,
    )


@timing("day21")
def main() -> int:
    i = InputReader(2016, 21).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1("abcde", example)("decab")
        assert part1("abcdefgh", puzzle)("hcdefbag")

    def s2() -> None:
        assert part2("decab", example)("abcde")
        assert part2("hcdefbag", puzzle)("abcdefgh")
        assert part2("fbgdceah", puzzle)("fbhaegdc")

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
