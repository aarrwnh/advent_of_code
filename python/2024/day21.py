import sys

from support import InputReader, asserter, timing

P = tuple[int, int]
Keys = dict[P, str]

KEYPAD_NUMS: tuple[P, Keys] = ((2,3), {
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
    (0, 1): "4",
    (1, 1): "5",
    (2, 1): "6",
    (0, 2): "1",
    (1, 2): "2",
    (2, 2): "3",
    # (0, 3)
    (1, 3): "0",
    (2, 3): "A",
})

KEYPAD_DIRS: tuple[P, Keys] = ((2,0), {
    # (0, 0)
    (1, 0): "^",
    (2, 0): "A",
    (0, 1): "<",
    (1, 1): "v",
    (2, 1): ">",
})


def simulate(codes: list[str], current_keypad: int) -> int:
    best: dict[tuple[P, P, int], int] = {}

    def from_to(src: P, dst: P, skip_blank: P, layer_depth: int) -> int:
        n = best.get((src, dst, layer_depth), None)
        src0 = src
        if n is None:
            n = sys.maxsize
            todo = [(src0, "")]

            while todo:
                src, path = todo.pop()
                if src == dst:
                    n = min(n, shortest(KEYPAD_DIRS, f"{path}A", layer_depth - 1))
                    continue
                if src == skip_blank:
                    continue

                if src[0] > dst[0]:
                    todo.append(((src[0] - 1, src[1]), f"{path}<"))
                elif src[0] < dst[0]:
                    todo.append(((src[0] + 1, src[1]), f"{path}>"))

                if src[1] > dst[1]:
                    todo.append(((src[0], src[1] - 1), f"{path}^"))
                elif src[1] < dst[1]:
                    todo.append(((src[0], src[1] + 1), f"{path}v"))

            best[(src0, dst, layer_depth)] = n
        return n

    def shortest(keys: tuple[P, Keys], sequence: str, layer_depth: int) -> int:
        if layer_depth == 0:
            return len(sequence)

        # start = None
        # for p, numkey in keys.items():
        #     if numkey == "A":
        #         start = p
        #         break
        # assert start is not None

        n = 0
        start = keys[0]
        skip: P = (0, start[1])

        for char in sequence:
            for p, numkey in keys[1].items():
                if numkey == char:
                    n += from_to(start, p, skip, layer_depth)
                    start = p

        return n

    return sum(
        # keypad count: 1 numerical + n directional
        int(code[:-1]) * shortest(KEYPAD_NUMS, code, current_keypad + 1)
        for code in codes
    )


@asserter
def part1(lines: list[str]) -> int:
    return simulate(lines, 2)


@asserter
def part2(lines: list[str]) -> int:
    return simulate(lines, 25)


@timing("day21")
def main() -> int:
    i = InputReader(2024, 21).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(126384)
        assert part1(puzzle)(105458)

    def s2() -> None:
        assert part2(example)(154115708116294)
        assert part2(puzzle)(129551515895690)

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
