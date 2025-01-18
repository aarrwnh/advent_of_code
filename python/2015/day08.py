import ast
import sys

from support import InputReader, asserter, timing


@asserter
def part1(lines: list[str]) -> int:
    return sum(len(line) - len(ast.literal_eval(line)) for line in lines)


@asserter
def part2(lines: list[str]) -> int:
    def escape(text: str, repl: str) -> str:
        for ch in repl:
            text = text.replace(ch, "\\" + ch)
        return f'"{text}"'

    return sum(len(escape(line, '\\"')) - len(line) for line in lines)


@timing("day8")
def main() -> int:
    i = InputReader(2015, 8).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(12)
        assert part1(puzzle)(1333)

    def s2() -> None:
        assert part2(example)(19)
        assert part2(puzzle)(2046)

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
