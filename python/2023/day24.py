import sys
from typing import NamedTuple

from support import InputReader, asserter, timing

P = tuple[float, float]


class Vec3(NamedTuple):
    x: float
    y: float
    z: float


class Vec2(NamedTuple):
    x: float
    y: float


def crossing(a: Vec2, b: Vec2) -> float:  # vector cross
    return (a[0] * b[1]) - (a[1] * b[0])


class Hailstone(NamedTuple):
    position: Vec3
    velocity: Vec3

    @classmethod
    def parse(cls, line: str) -> "Hailstone":
        p_s, v_s = line.split(" @ ")
        position = map(float, p_s.split(", "))
        velocity = map(float, v_s.split(", "))
        return cls(Vec3(*position), Vec3(*velocity))

    def intersection_xy(self, other: "Hailstone") -> Vec2 | None:
        a = Vec2(self.velocity.x, self.velocity.y)
        b = Vec2(other.velocity.x, other.velocity.y)

        div = crossing(a, b)
        if div == 0:
            return None  # not intersecting

        d = Vec2(other.position.x - self.position.x, other.position.y - self.position.y)
        u = crossing(d, b) / div

        return Vec2(
            self.position.x + (self.velocity.x * u),
            self.position.y + (self.velocity.y * u),
        )

    def in_range(self, p: Vec2) -> bool:
        dx = p.x - self.position.x
        dy = p.y - self.position.y
        return (dx > 0) == (self.velocity.x > 0) and (dy > 0) == (self.velocity.y > 0)


@asserter
@timing("part1")
def part1(lines: list[str], area: tuple[float, float] = (0.0, 0.0)) -> int:
    ## m = (y2 - y1) / (x2 - x1)
    ## y = mx + b
    stones: list[Hailstone] = [Hailstone.parse(line) for line in lines]

    def inside_test_area(p: Vec2) -> bool:
        return area[0] <= p.x <= area[1] and area[0] <= p.y <= area[1]

    intersections = 0
    for i, h1 in enumerate(stones):
        for h2 in stones[i + 1 :]:
            point = h1.intersection_xy(h2)
            if (
                point is not None
                and inside_test_area(point)
                and h1.in_range(point)
                and h2.in_range(point)
            ):
                intersections += 1

    return intersections


@asserter
@timing("part2")
def part2(lines: list[str]) -> int:
    stones: list[Hailstone] = [Hailstone.parse(line) for line in lines]

    def find_match_vel(dvel: int, pv: int) -> list[int]:
        matches = []
        for i in range(-300, 300):
            if i != pv and dvel % (i - pv) == 0:
                matches.append(i)
        return matches

    def get_intersect(a: list[int], b: list[int]) -> list[int]:
        result = []
        for val in a:
            if val in b:
                result.append(val)
        return result

    cand_x: list[int] = []
    cand_y: list[int] = []
    cand_z: list[int] = []
    for i in range(len(stones) - 1):
        a = stones[i]
        for j in range(i + 1, len(stones)):
            b = stones[j]
            if a.velocity.x == b.velocity.x:
                candidates = find_match_vel(
                    int(b.position.x - a.position.x), int(a.velocity.x)
                )
                if len(cand_x) == 0:
                    cand_x = candidates
                else:
                    cand_x = get_intersect(cand_x, candidates)

            if a.velocity.y == b.velocity.y:
                candidates = find_match_vel(
                    int(b.position.y - a.position.y), int(a.velocity.y)
                )
                if len(cand_y) == 0:
                    cand_y = candidates
                else:
                    cand_y = get_intersect(cand_y, candidates)

            if a.velocity.z == b.velocity.z:
                candidates = find_match_vel(
                    int(b.position.z - a.position.z), int(a.velocity.z)
                )
                if len(cand_z) == 0:
                    cand_z = candidates
                else:
                    cand_z = get_intersect(cand_z, candidates)

    # print(cand_x, cand_y, cand_z)

    cand = []
    for cx in cand_x:
        for cy in cand_y:
            for cz in cand_z:
                rock = Vec3(cx, cy, cz)
                a, b = stones[0], stones[2]
                ma = (a.velocity.y - rock.y) / (a.velocity.x - rock.x)
                mb = (b.velocity.y - rock.y) / (b.velocity.x - rock.x)
                ca = a.position.y - (ma * a.position.x)
                cb = b.position.y - (mb * b.position.x)
                xpos = (cb - ca) / (ma - mb)
                ypos = ma * xpos + ca
                time = (xpos - a.position.x) / (a.velocity.x - rock.x)
                zpos = a.position.z + (a.velocity.z - rock.z) * time
                cand.append(sum([int(xpos), int(ypos), int(zpos)]))

    # print(cand)

    return cand[0]


def main() -> int:
    i = InputReader(2023, 24).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample, area=(7, 27))(2)
        assert part1(puzzle, area=(200000000000000, 400000000000000))(24192)

    def s2() -> None:
        assert part2(sample)(47)
        assert part2(puzzle)(664822352550558)

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
