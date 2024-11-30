import collections
import sys
from operator import itemgetter
from typing import NamedTuple

from support import InputReader, asserter, timing


class Brick(NamedTuple):
    # left
    x1: int
    y1: int
    z1: int
    # right
    x2: int
    y2: int
    z2: int

    supported_by: set[int]

    @classmethod
    def parse(cls, line: str) -> "Brick":
        left_s, right_s = line.split("~")
        left = [int(x) for x in left_s.split(",")]
        right = [int(x) for x in right_s.split(",")]
        return cls(left[0], left[1], left[2], right[0], right[1], right[2], set())

    def collides(self, other: "Brick") -> bool:
        return (
            self.x1 <= other.x2
            and other.x1 <= self.x2
            and self.y1 <= other.y2
            and other.y1 <= self.y2
        )


def simulate(lines: list[str]) -> tuple[list[Brick], set[int]]:
    bricks = [Brick.parse(line) for line in lines]
    by_height = collections.deque(
        sorted([(b.z1, i) for i, b in enumerate(bricks)], key=itemgetter(0))
    )

    removable = set(i for i in range(len(bricks)))
    ground: set[tuple[int, ...]] = set()
    # fb  falling brick
    # gb  ground brick
    while by_height:
        _, fb_index = by_height.popleft()
        nheight = 0
        current_bottom = 0
        supporter: list[int] = []

        # we need to start from ground each iter
        for gb_top, gb_index in reversed(sorted(list(ground), key=itemgetter(0))):
            if nheight > 0 and gb_top < current_bottom:
                break

            # print(
            #     f"#{fb_index} falling towards {gb_index}",
            #     bricks[fb_index].collides(bricks[gb_index]),
            # )
            if bricks[fb_index].collides(bricks[gb_index]):
                # print(f"#{fb_index} hits {gb_index}")
                height = bricks[fb_index].z2 - bricks[fb_index].z1
                nheight = gb_top + 1 + height
                current_bottom = gb_top
                supporter.append(gb_index)
                bricks[fb_index].supported_by.add(gb_index)

        if nheight == 0:
            height = bricks[fb_index].z2 - bricks[fb_index].z1 + 1
            ground.add((height, fb_index))
        else:
            ground.add((nheight, fb_index))
            # print(f"brick #{fb_index} is supported by {supporter} at {nheight}")

        if len(supporter) == 1:
            removable -= {supporter[0]}

    return bricks, removable


@asserter
@timing("part1")
def part1(lines: list[str]) -> int:
    _, removable = simulate(lines)
    return len(removable)


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    bricks, removable = simulate(lines)

    def will_fall(removing: int, index: int) -> bool:
        if removing == index:
            return True

        for ii in bricks[index].supported_by:
            if not will_fall(removing, ii):
                return False

        return len(bricks[index].supported_by) > 0

    total_falling = 0
    for i in range(len(bricks)):
        if i in removable:
            continue

        for j in range(len(bricks)):
            if i != j and will_fall(i, j):
                total_falling += 1
                # print(f"if {i} is removed, {j} will fall")

    return total_falling


def main() -> int:
    i = InputReader(2023, 22).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(5)
        assert part1(puzzle)(413)

    def s2() -> None:
        assert part2(sample)(7)

    def s3() -> None:
        assert part2(puzzle)(41610)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case [_, "3"]:
            s3()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
