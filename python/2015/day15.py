import sys
from typing import NamedTuple

from support import InputReader, asserter, timing


class Ingredient(NamedTuple):
    # name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def get_prop(self, name: str) -> int:
        return self.__getattribute__(name)


def partition(n: int, size: int) -> list[list[int]]:
    if size == 0:
        return [[]]
    return [item + [i] for i in range(1, n + 1) for item in partition(n - i, size - 1)]


def partitions(n: int, d: int):
    for p in partition(n, d - 1):
        yield [n - sum(p)] + p


def sum_props(
    names: list[str], ingredients: dict[str, Ingredient], comb: list[int]
) -> int:
    score = 1
    for prop_name in ["capacity", "durability", "flavor", "texture"]:
        current = 0
        for i, amount in enumerate(comb):
            current += ingredients[names[i]].get_prop(prop_name) * amount
        if current < 0:
            return 0
        score *= current
    return score


def parse(lines: list[str]) -> tuple[list[str], dict[str, Ingredient]]:
    ingredients: dict[str, Ingredient] = {}
    names: list[str] = []
    for line in lines:
        ing, props = line.split(": ")
        p = [int(v) for v in props.replace(",", "").split(" ")[1::2]]
        ingredients[ing] = Ingredient(*p)
        names.append(ing)
    return names, ingredients


TEASPOONS = 100


@asserter
def part1(lines: list[str]) -> int:
    names, ingredients = parse(lines)
    best = 0

    for comb in partitions(TEASPOONS, len(names)):
        score = sum_props(names, ingredients, comb)
        best = max(best, score)

    return best


@asserter
def part2(lines: list[str]) -> int:
    names, ingredients = parse(lines)
    best = 0

    for comb in partitions(TEASPOONS, len(names)):
        calories = sum(
            ingredients[names[i]].calories * amount for i, amount in enumerate(comb)
        )
        if calories == 500:
            score = sum_props(names, ingredients, comb)
            best = max(best, score)

    return best


@timing("day15")
def main() -> int:
    i = InputReader(2015, 15).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(62842880)
        assert part1(puzzle)(18965440)

    def s2() -> None:
        assert part2(example)(57600000)
        assert part2(puzzle)(15862900)

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
