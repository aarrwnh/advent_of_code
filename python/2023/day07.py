from collections import deque

from support import InputReader, asserter, timing

STR1 = "  23456789TJQKA"
STR2 = " J23456789T QKA"


# class Hand:
#     kind: int
#     strength: int

#     def __init__(self, kind: int, strength: int) -> None:
#         self.kind = kind
#         self.strength = strength


def count_to_kind(count: list[int]) -> int:
    match count:
        case [5]:  # five
            label = 6
        case [4]:  # four
            label = 5
        case [2, 3] | [3, 2]:  # full
            label = 4
        case [3]:  # three
            label = 3
        case [2, 2]:  # two
            label = 2
        case [2]:  # one
            label = 1
        case []:  # high
            label = 0
        case _:
            raise AssertionError("not impl", count)
    return label


def measure_hand_part1(hand: str, mapping: str) -> tuple[int, list[int], int]:
    nums = [mapping.index(x) for x in hand]
    hand_kind = sum([len([0 for y in nums if x == y]) for x in nums])
    return hand_kind, nums, 0

    # h = {mapping.index(c): hand.count(c) for c in set(hand) if hand.count(c) > 1}
    # hand_kind = count_to_kind(list(h.values()))

    # score = hand_kind
    # for x in cards:
    #     score = (score << 4) | x

    # return hand_kind, cards, score


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    total = 0
    data: list[tuple[int, int, list[int], int]] = []
    for line in lines:
        hand, bid_s = line.split(" ")
        data.append((int(bid_s), *measure_hand_part1(hand, STR1)))

    data = sorted(data, key=lambda x: (x[1], x[2]))
    for j, (bid, _, _, _) in enumerate(data, 1):
        total += j * bid

    return total


def combinator(hand: str) -> set[str]:
    cand = "AKQT98765432"

    idx = 0
    current = hand[idx]

    todo: deque[tuple[str, ...]]
    initial: list[tuple[str]] = []

    if current == "J":
        for x in cand:
            initial.append((x,))
    else:
        initial.append((current,))

    todo = deque(initial)
    possible: set[str] = set()

    def readd(value: str) -> None:
        if len(value) == len(hand):
            possible.add(value)
        else:
            todo.append((value,))

    while todo:
        (n,) = todo.popleft()
        if len(n) - 1 > idx:
            idx += 1
        if idx > len(hand):
            break

        if hand[idx + 1] == "J":
            for c in cand:
                readd(n + c)
        else:
            readd(n + hand[idx + 1])

    return possible


def measure_hand_part2(hand: str, mapping: str) -> tuple[int, list[int]]:
    nums = [mapping.index(x) for x in hand]
    rest_letters = sorted([len([0 for y in nums if x == y]) for x in nums if x != 1])
    j_count = 5 - len(rest_letters)
    rest_max = rest_letters[-1] if len(rest_letters) > 0 else 0
    rest_score = sum(rest_letters)
    score = (j_count * rest_max) + (rest_max + j_count) * j_count
    return score + rest_score, nums


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    # TODO: ?
    def find_best(hand: str) -> tuple[int, list[int]]:
        possible: list[tuple[int, list[int], int]] = []
        _, joker_nums, _ = measure_hand_part1(hand, STR2)

        for possible_hand in combinator(hand):
            possible.append((*measure_hand_part1(possible_hand, STR2),))

        po = sorted(possible, key=lambda x: (x[2], x[1]))
        _, _, score = po.pop()
        # print(hand, "=>", found_hand)
        return (
            score,
            joker_nums,
        )

    data: list[tuple[int, int, list[int]]] = []
    for line in lines:
        hand, bid_s = line.split(" ")
        # if "J" in hand:
        #     data.append((hand, int(bid_s), *find_best(hand)))
        # else:
        data.append((int(bid_s), *measure_hand_part2(hand, STR2)))

    total = 0
    data = sorted(data, key=lambda x: (x[1], x[2]))
    for j, (bid, _, _) in enumerate(data, 1):
        total += j * bid

    return total


def main() -> int:
    i = InputReader(2023, 7)
    sample = i.lines("sample")
    puzzle = i.lines("puzzle")

    part1(sample)(6440)
    part1(puzzle)(250058342)

    part2(sample)(5905)
    part2(puzzle)(250506580)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
