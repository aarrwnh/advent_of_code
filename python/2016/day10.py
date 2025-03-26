import collections

from support import InputReader, asserter, timing


@asserter
def solve(instructions: list[str]) -> tuple[int, int]:
    tbl: dict[str, list[int]] = collections.defaultdict(list)
    target = {17, 61}
    compare_bot = 0
    while len(instructions) > 0:
        cand: list[str] = []
        for inst in instructions:
            if inst.startswith("value"):
                _, mp, _, _, _, bot = inst.split()
                tbl[f"bot_{bot}"].append(int(mp))
            elif inst.startswith("bot"):
                _, bot, _, _, _, ty_a, a, _, _, _, ty_b, b = inst.split()
                v = tbl[f"bot_{bot}"]

                if len(v) == 2:
                    low, high = sorted(v)
                    v.clear()

                    tbl[f"{ty_a}_{a}"].append(low)
                    tbl[f"{ty_b}_{b}"].append(high)

                    # part 1:
                    if len(target & {low, high}) == 2:
                        compare_bot = int(bot)
                else:
                    cand.append(inst)
            else:
                raise AssertionError("notimplemented")
        instructions = cand

    # part 2:
    output = 1
    for i in range(3):
        output *= tbl[f"output_{i}"][0]

    return compare_bot, output


@timing("day10")
def main() -> int:
    i = InputReader(2016, 10).lines

    puzzle = i("puzzle")

    assert solve(puzzle)((157, 1085))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
