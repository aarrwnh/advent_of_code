import collections
import math
import sys

from support import InputReader, asserter, timing


class Module:
    def __init__(self, kind: str, src: str, dst: list[str]) -> None:
        self.kind = kind
        self.src = src
        self.dst = dst
        self.state = 0
        self.conjunctions: dict[str, int] = {}

    def __repr__(self) -> str:
        return f"{self.dst}::{self.conjunctions}"


def parse(lines: list[str]) -> dict[str, Module]:
    conjunctions: dict[str, dict[str, int]] = {}
    parsed: dict[str, Module] = {}

    for line in lines:
        left, right_s = line.split(" -> ")
        right = right_s.split(", ")
        symbol, name = left[0], left[1:]
        match symbol:
            case "%" | "&":
                parsed[name] = Module(symbol, name, right)
                if symbol == "&":
                    conjunctions[name] = {}
            case _:
                parsed["broadcast"] = Module("broadcast", left, right)

    # add flip-flop default state for all conjunctions
    for m in parsed:
        for n in parsed[m].dst:
            if n in conjunctions:
                conjunctions[n][m] = 0

    # fillup module conjunctions
    for m in parsed:
        if m in conjunctions:
            parsed[m].conjunctions = conjunctions[m]

    return parsed


def send_pulse(
    parsed: dict[str, Module], needles: list[str] | None = None
) -> list[int]:
    initial = [("button", "broadcast", 0)]

    todo: collections.deque[tuple[str, str, int]]
    todo = collections.deque(initial)

    found_pulse = False
    count = [0, 0]

    while todo:
        src, dest, pulse = todo.popleft()

        count[pulse] += 1
        if dest not in parsed:
            # skip on missing module
            continue

        cmodule = parsed[dest]
        match cmodule.kind:
            case "broadcast":
                for c in cmodule.dst:
                    todo.append((dest, c, 0))
            case "%":
                if pulse == 0:
                    cmodule.state = not cmodule.state
                    for c in cmodule.dst:
                        todo.append((dest, c, cmodule.state))
            case "&":
                cmodule.conjunctions[src] = pulse
                sending = all(v == 1 for v in cmodule.conjunctions.values())

                # part2:
                # The machine turns on when a single low pulse is sent to rx.
                if sending ^ 0 == 0 and needles and len(needles) > 0:
                    for key in needles:
                        if key == dest:
                            found_pulse = True

                for c in cmodule.dst:
                    todo.append((dest, c, sending ^ 1))

    if found_pulse:
        return [-1, -1]  # fake count we don't need for part2
    return count


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    parsed = parse(lines)

    low = high = 0

    for _ in range(1000):
        a, b = send_pulse(parsed)
        low += a
        high += b

    return low * high


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    parsed = parse(lines)

    needles: list[str] = []
    for m in parsed:
        # find source module for rx first
        # &lb -> rx
        #   ^
        if "rx" in parsed[m].dst:
            for n in parsed:
                # and then all keys which could reach rx
                # &rz -> lb
                #   ^
                if m in parsed[n].dst:
                    needles.append(n)
            break

    assert len(needles) > 0, "no `rx` module found in puzzle"

    cycles = []
    loop_count = 0
    while True:
        loop_count += 1
        if send_pulse(parsed, needles)[0] == -1:
            cycles.append(loop_count)
            if len(cycles) == len(needles):
                break

    return math.lcm(*cycles)


def main() -> int:
    i = InputReader(2023, 20).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(
            [
                "broadcaster -> a",
                "%a -> inv, con",
                "&inv -> b",
                "%b -> con",
                "&con -> output",
            ]
        )(11687500)
        assert part1(sample)(32000000)
        assert part1(puzzle)(817896682)

    def s2() -> None:
        assert part2(puzzle)(250924073918341)

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
