import re
import sys
from collections.abc import Generator
from typing import NamedTuple

from support import InputReader, asserter, timing

s = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


class Item(NamedTuple):
    name: str
    cost: int
    dmg: int
    armor: int


class Character(NamedTuple):
    hp: int
    dmg: int
    armor: int


RE = re.compile(r"(.+?)\s\s*(\d+)\s*(\d+)\s*(\d+)")

SHOP: dict[str, list[Item]] = {}
for c in s.split("\n\n"):
    h, *rest = c.strip().splitlines()
    type_ = h.split(":")[0]
    SHOP[type_] = []
    for line in rest:
        a = RE.match(line)
        if a is None:
            continue
        itm = Item(a.groups()[0], *(int(x) for x in a.groups()[1:]))
        SHOP[type_].append(itm)
W = SHOP["Weapons"]
A = SHOP["Armor"]
R = SHOP["Rings"]
mi = len(R) // 2
R_DMG = R[:mi]
R_DEF = R[mi:]


def sum_stats(items: tuple[Item, ...]) -> list[int]:
    stats = [0, 0, 0]
    for itm in items:
        stats[0] += itm.cost
        stats[1] += itm.dmg
        stats[2] += itm.armor
    return stats


def simulate(player: Character, enemy: Character) -> int:
    p_dmg = player.dmg - enemy.armor
    if p_dmg <= 0:
        return False

    e_dmg = enemy.dmg - player.armor
    if e_dmg <= 0:
        return True

    p_turns, rem = divmod(enemy.hp, p_dmg)
    p_turns += bool(rem)
    e_turns, rem = divmod(player.hp, e_dmg)
    e_turns += bool(rem)

    return p_turns <= e_turns


def item_combinations() -> Generator[tuple[Item, ...]]:
    for weapon in W:
        for armor in A:
            yield weapon, armor
            for r1 in R:
                yield weapon, armor, r1
            for r1, r2 in zip(R_DMG, R_DEF, strict=True):
                yield weapon, armor, r1, r2


def parse(input: str) -> Character:
    return Character(*[int(x.split(": ")[1]) for x in input.strip().splitlines()])


@asserter
def part1(input: str) -> int:
    enemy = parse(input)
    min_cost = sys.maxsize
    for items in item_combinations():
        cost, dmg, armor = sum_stats(items)
        p1 = Character(100, dmg, armor)
        if simulate(p1, enemy):
            min_cost = min(min_cost, cost)
    return min_cost


@asserter
def part2(input: str) -> int:
    enemy = parse(input)
    max_cost = 0
    for items in item_combinations():
        cost, dmg, armor = sum_stats(items)
        p1 = Character(100, dmg, armor)
        if not simulate(p1, enemy):
            max_cost = max(max_cost, cost)
    return max_cost


@timing("day21")
def main() -> int:
    i = InputReader(2015, 21).raw

    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(puzzle)(121)

    def s2() -> None:
        assert part2(puzzle)(201)

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
