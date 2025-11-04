import collections
import math
from typing import NamedTuple

from support import InputReader, asserter, timing


class Value(NamedTuple):
    bot: int
    mp: int


class Action(NamedTuple):
    bot: int
    a: int
    a_ty: int  # bot | output
    b: int
    b_ty: int


BOT = 0x100
OUTPUT = 0x200


def ty_to_val(ty: str) -> int:
    if ty == "bot":
        return BOT
    return OUTPUT


def parse(instructions: list[str]) -> list[Value | Action]:
    tbl: list[Value | Action] = []
    bots: list[Action] = []
    for inst in instructions:
        if inst.startswith("value"):
            _, mp, _, _, _, bot = inst.split()
            tbl.append(Value(bot=int(bot), mp=int(mp)))
        elif inst.startswith("bot"):
            _, bot, _, _, _, ty_a, a, _, _, _, ty_b, b = inst.split()
            bots.append(Action(
                bot=int(bot),
                a=int(a),
                a_ty=ty_to_val(ty_a),
                b=int(b),
                b_ty=ty_to_val(ty_b)
            ))
    return tbl + sorted(bots, key=lambda x: x.a_ty)


@asserter
def solve(instructions: list[str]) -> tuple[int, int]:
    instructions0 = parse(instructions)
    tbl: dict[int, set[int]] = collections.defaultdict(set)
    target = {17, 61}
    compare_bot = 0
    while len(instructions0) > 0:
        cand: list[Value | Action] = []
        for inst in instructions0:
            if isinstance(inst, Value):
                tbl[BOT | inst.bot].add(inst.mp)
            elif isinstance(inst, Action):
                v = tbl.get(BOT | inst.bot, None)
                if v is not None and len(v) == 2:
                    low, high = sorted(v)

                    tbl[inst.a_ty | inst.a].add(low)
                    tbl[inst.b_ty | inst.b].add(high)

                    # part 1:
                    if target == {low, high}:
                        compare_bot = inst.bot
                else:
                    cand.append(inst)
            else:
                raise AssertionError("notimplemented")
        instructions0 = cand

    # part 2:
    outputs = tuple(tuple(tbl[OUTPUT | i])[0] for i in range(3))

    return compare_bot, math.prod(outputs)


@timing("day10")
def main() -> int:
    i = InputReader(2016, 10).lines

    puzzle = i("puzzle")

    assert solve(puzzle)((157, 1085))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
