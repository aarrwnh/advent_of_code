import math
import re
import sys
from typing import NamedTuple

from support import InputReader, asserter, timing


class Condition(NamedTuple):
    category: str
    sign: str
    val: int


class Rule(NamedTuple):
    condition: Condition | None
    dest: str
    accepted: bool

    def compare(self, ratings: dict[str, int]) -> bool:
        if self.condition is not None:
            left = ratings[self.condition.category]
            match self.condition.sign:
                case ">":
                    return left > self.condition.val
                case "<":
                    return left < self.condition.val
        return self.accepted


def parse(input: str) -> tuple[list[dict[str, int]], dict[str, list[Rule]]]:
    workflows_s, ratings_s = input.split("\n\n")
    ratings: list[dict[str, int]] = []
    for rating in ratings_s.splitlines():
        b = {}
        for a in rating[1:-1].split(","):
            k, v = a.split("=")
            b[k] = int(v)
        ratings.append(b)

    workflows: dict[str, list[Rule]] = {}
    for w in workflows_s.splitlines():
        name, rest_s = w.split("{")
        rules: list[Rule] = []
        for rule in rest_s[:-1].split(","):
            match rule.split(":"):
                case [dest]:  # rfg
                    r = Rule(condition=None, dest=dest, accepted=dest != "R")
                case [condition, dest]:  # a<2006:qkq
                    category, sign, val = re.split(r"([><])", condition, maxsplit=1)
                    c = Condition(category, sign, int(val))
                    r = Rule(c, dest, dest != "R")
                case _:
                    raise AssertionError("unreachable")
            rules.append(r)

        workflows[name] = rules
    return ratings, workflows


@asserter
@timing("part1")
def part1(input: str) -> int:
    ratings, workflows = parse(input)

    def compute(current: str, rating: dict[str, int]) -> int:
        t = 0
        for r in workflows[current]:
            if r.compare(rating):
                if r.dest == "A":
                    return sum(rating.values())
                elif r.dest == "R":
                    break
                else:
                    t += compute(r.dest, rating)
                    break
        return t

    return sum(compute("in", rating) for rating in ratings)


# slow: dont'
class Range:
    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def copy(self) -> "Range":
        return Range(self.start, self.stop)

    def __repr__(self) -> str:
        return f"range({self.start}, {self.stop})"

    def len(self) -> int:
        return 1 + self.stop - self.start


@asserter
@timing("part2")
def part2(input: str) -> int:
    _, workflows = parse(input)

    def compute(w: str, ratings: dict[str, range]) -> int:
        total = 0
        workflow = workflows[w]
        for r in workflow:
            nratings = ratings.copy()
            # nratings = {k: v.copy() for k, v in ratings.items()}
            if r.condition is not None:
                (key, sign, val) = r.condition
                match sign:
                    case "<":
                        # nratings[key].stop = val - 1
                        # ratings[key].start = val
                        nratings[key] = range(nratings[key].start, val - 1)
                        ratings[key] = range(val, ratings[key].stop)
                    case ">":
                        # nratings[key].start = val + 1
                        # ratings[key].stop = val
                        nratings[key] = range(val + 1, nratings[key].stop)
                        ratings[key] = range(ratings[key].start, val)

            if r.dest == "A":
                total += math.prod([1 + x.stop - x.start for x in nratings.values()])
            elif r.dest == "R":
                pass
            else:
                total += compute(r.dest, nratings)

        return total

    ratings = {
        "x": range(1, 4000),
        "m": range(1, 4000),
        "a": range(1, 4000),
        "s": range(1, 4000),
    }
    return compute("in", ratings)


def main() -> int:
    i = InputReader(2023, 19).raw

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(19114)
        assert part1(puzzle)(353046)

    def s2() -> None:
        assert part2(sample)(167409079868000)
        assert part2(puzzle)(125355665599537)

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
