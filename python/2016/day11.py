import heapq
import itertools
import re
import sys
from collections.abc import Generator

from support import InputReader, asserter, timing

THING = re.compile(r"(?P<name>[\w\-]+) (?P<type>generator|microchip)")

GENERATOR = ord("g")
MICROCHIP = ord("m")


Item = tuple[int, int]
Floor = frozenset[Item]
Floors = tuple[Floor, ...]


class State:
    elevator: int
    floors: Floors

    def __init__(self, floors: Floors, elevator: int = 0):
        self.elevator = elevator
        self.floors = floors

    @classmethod
    def parse(cls, lines: list[str]) -> tuple[int, State]:
        item = 0xF
        items: dict[str, int] = {}
        floors: list[Floor] = []

        for line in lines:
            floor: set[Item] = set()
            for m in THING.finditer(line):
                typ = ord(m.group("type")[0])
                name_s = m.group("name").replace("-compatible", "")
                if name_s not in items:
                    items[name_s] = item
                    item <<= 1
                floor.add((typ, items[name_s]))
            floors.append(frozenset(sorted(floor)))

        return len(items) * 2, cls(floors=tuple(floors))

    def __lt__(self, other: State):
        return self.elevator < other.elevator

    def __eq__(self, other: State):
        return self.__key() == other.__key()

    def __key(self):
        return (self.elevator, self.floors)

    def __hash__(self) -> int:
        return hash(self.__key())

    # def __str__(self) -> str:
    #     a = [list(item_to_str(x) for x in floor) for floor in self.floors]
    #     return f"step={self.step} floor={self.floor} :: {a}"

    def valid_floors(self) -> bool:
        # F4 .  .  .  .  .
        # F3 .  .  .  LG .
        # F2 .  HG .  .  .
        # F1 E  .  HM .  LM

        # for floor in floors:
        #     gns = {get_name(x) for x in floor if get_type(x) == GENERATOR}
        #     mcr = {get_name(x) for x in floor if get_type(x) == MICROCHIP}
        #     if len(gns) == 0 or len(mcr) == 0:
        #         continue
        #     for m in mcr:
        #         if all(x == m for x in gns):
        #             return False
        # else:
        #     return True
        for floor in self.floors:
            if not floor:
                continue
            gns = {name for typ, name in floor if typ == GENERATOR}
            for typ, name in floor:
                if typ == GENERATOR:  # noqa: SIM114
                    continue
                elif any(g for g in gns if name == g):
                    continue
                elif len(gns) > 0:
                    return False
        else:
            return True

    def next(self) -> Generator[State]:
        for n in self.next_pos(self.elevator):
            for c in self.combinations():
                c = frozenset(c)
                floors = list(self.floors)
                floors[self.elevator] -= c
                floors[n] = frozenset(sorted(floors[n] | c))

                yield State(elevator=n, floors=tuple(floors))

    def combinations(self) -> Generator[tuple[Item, ...]]:
        items = self.floors[self.elevator]
        # prioritize moving with 2 items
        yield from itertools.combinations(items, 2)
        yield from tuple((c1,) for c1 in items)

    @staticmethod
    def next_pos(pos: int) -> Generator[int]:
        for i in [pos + 1, pos - 1]:
            if 0 <= i < 4:
                yield i

    def check_top_floor(self, total_items: int, floor: int) -> bool:
        return (self.elevator == floor
                and total_items == len(self.floors[floor]))


def solve(lines: list[str]) -> int:
    item_count, initial = State.parse(lines)
    top_floor = len(lines) - 1

    queue: list[tuple[int, State]] = [(0, initial)]
    best = {initial: 0}

    while queue:
        _, current = heapq.heappop(queue)

        if current.check_top_floor(item_count, top_floor):
            return best[current]

        n_step = best[current] + 1
        for cand in current.next():
            if not (cand not in best or n_step < best[cand]):
                continue
            if not cand.valid_floors():
                continue
            best[cand] = n_step
            priority = n_step - (len(cand.floors[top_floor]) << 4)
            heapq.heappush(queue, (priority, cand))

    raise AssertionError("unreachable")


@asserter
def part1(lines: list[str]) -> int:
    return solve(lines)


@asserter
def part2(lines: list[str]) -> int:
    lines[0] += (
        "elerium generator"
        + "elerium-compatible microchip"
        + "dilithium generator"
        + "dilithium-compatible microchip"
    )
    return solve(lines)


@timing("day11")
def main() -> int:
    i = InputReader(2016, 11).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(11)
        assert part1(puzzle)(31)

    def s2() -> None:
        assert part2(puzzle)(55)

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
