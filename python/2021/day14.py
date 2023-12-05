from typing import Dict, List, Tuple
import os
import re
import collections
from support import timing


def read_file(filename: str) -> Tuple[str, List[List[str]]]:
    lines: List[str] = []
    path = os.path.dirname(__file__) + "/" + filename
    polymer, rules = open(path, "r").read().split("\n\n")
    rules = [rule.split(" -> ") for rule in rules.strip().split("\n")]
    return (polymer, rules)


@timing()
def brute(data: Tuple[str, List[List[str]]], step: int) -> int:
    polymer, rules = data

    if step > 20:
        return 0

    for _ in range(step):
        templ: Dict[int, str] = {}
        for rule in rules:
            pair, insertion = rule

            for idx in [m.start() for m in re.finditer("(?=" + pair + ")", polymer)]:
                templ[idx] = pair[0] + insertion + pair[1]

        out = []
        for _, t in sorted(templ.items(), key=lambda x: x[0]):
            if len(out) > 1:
                if out[-1] == t[0]:
                    t = t[1:3]

            for w in [*t]:
                out.append(w)

        polymer = "".join(out)

    counts = sorted(v for v in collections.Counter(polymer).values())
    return counts[-1] - counts[0]


@timing()
def compute(data: Tuple[str, List[List[str]]], steps: int) -> int:
    polymer, rules = data

    patterns = {}
    for pair, insertion in rules:
        patterns[pair] = insertion

    counter = collections.Counter()
    for i in range(0, len(polymer) - 1):
        counter[polymer[i : i + 2]] += 1

    single_counter = collections.Counter()
    for i in range(steps):
        single_counter.clear()
        double_counter = collections.Counter()

        for k, v in counter.items():
            double_counter[f"{k[0]}{patterns[k]}"] += v
            double_counter[f"{patterns[k]}{k[1]}"] += v

            if i == steps - 1:
                single_counter[k[0]] += v
                single_counter[patterns[k]] += v

        single_counter[polymer[-1]] += 1
        counter = double_counter

    counts = [v[1] for v in single_counter.most_common()]
    return counts[0] - counts[-1]


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


def main() -> int:
    sample = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    check_result(1588, compute(sample, 10))
    check_result(2947, compute(puzzle, 10))

    check_result(2188189693529, compute(sample, 40))
    check_result(3232426226464, compute(puzzle, 40))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
