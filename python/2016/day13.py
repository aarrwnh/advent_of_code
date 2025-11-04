import collections
import sys

from support import asserter, timing

Coord = tuple[int, int]


def is_wall(fav: int, pos: Coord) -> bool:
    x, y = pos
    val = fav + ((x ** 2) + (3 * x) + (2 * x * y) + y + (y ** 2))
    return val.bit_count() & 1 == 1


@asserter
def solve(fav: int, start: Coord, end: Coord) -> tuple[int, int]:
    size = max(end) + 1  # ?

    queue = collections.deque([(0, start)])
    distinct: dict[Coord, int] = {(start): 0}
    fewest_steps = sys.maxsize

    while queue:
        step, pos = queue.popleft()

        if pos == end:
            fewest_steps = min(step, fewest_steps)
            continue

        (x, y) = pos
        for n in [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]:
            n_step = step + 1
            if (
                0 <= n[0] <= size and 0 <= n[1] <= size
                and not is_wall(fav, n)
                and n_step < distinct.get(n, sys.maxsize)
            ):
                queue.append((n_step, n))
                distinct[n] = n_step

    return fewest_steps, sum(1 for x in distinct.values() if x <= 50)


@timing("day13")
def main() -> int:
    assert solve(10, (1, 1), (7, 4))((11, 24))
    assert solve(1350, (1, 1), (31, 39))((92, 124))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
