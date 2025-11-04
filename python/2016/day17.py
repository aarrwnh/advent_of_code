# pyright: basic
import heapq
import sys
from _md5 import md5  # pyright: ignore[reportMissingImports]
from collections.abc import Generator

from support import InputReader, asserter, timing

DIRS = (
    ("U", 0, -1),
    ("D", 0, 1),
    ("L", -1, 0),
    ("R", 1, 0),
)

Coord = tuple[int, int]


def get_hash_prefix(passcode: str) -> tuple[str, ...]:
    hex = md5(passcode.encode()).hexdigest()
    # only the first four characters of the hash are used
    return tuple(hex[0:4])


def next_directions(
    coord: Coord, letters: tuple[str, ...]
) -> Generator[tuple[str, Coord]]:
    for ch, (dir, dx, dy) in zip(letters, DIRS, strict=True):
        if ord(ch) > 97:  # bcdef
            yield dir, (coord[0] + dx, coord[1] + dy)


def search(passcode: str, start: Coord, end: Coord) -> str:
    queue = [(0, start, "")]
    found = None
    max_len = 0
    while queue:
        step, pos, path = heapq.heappop(queue)
        if pos == end:
            length = len(path)
            if length > max_len:
                found = path
            max_len = max(max_len, length)
            break

        hash = get_hash_prefix(passcode + path)

        for dir, n in next_directions(pos, hash):
            n_path = path + dir
            if n is end or (0 <= n[0] < 4 and 0 <= n[1] < 4):
                heapq.heappush(queue, (step + 1, n, n_path))

    assert found is not None
    return found


@asserter
def part1(input: str) -> str:
    return search(input, (0, 0), (3, 3))


@asserter
def part2(input: str) -> int:
    end = (3, 3)
    max_len = [0]

    def _search(pos: Coord, path: str = "") -> str | None:
        if pos == end:
            return path

        hash = get_hash_prefix(input + path)
        for dir, n in next_directions(pos, hash):
            n_path = path + dir
            if n is end or (0 <= n[0] < 4 and 0 <= n[1] < 4):
                result = _search(n, n_path)
                if result is not None:
                    max_len[0] = max(max_len[0], len(result))

        return

    _search((0, 0))
    return max_len[0]


@timing("day17")
def main() -> int:
    i = InputReader(2016, 17).raw

    puzzle = i("puzzle").strip()

    def s1() -> None:
        assert part1(puzzle)("RDULRDDRRD")

    def s2() -> None:
        assert part2(puzzle)(752)

    def test() -> None:
        assert part1("ihgpwlah")("DDRRRD")
        assert part1("kglvqrro")("DDUDRLRRUDRD")
        assert part1("ulqzkmiv")("DRURDRUDDLLDLUURRDULRLDUUDDDRR")
        assert part2("ihgpwlah")(370)
        assert part2("kglvqrro")(492)
        assert part2("ulqzkmiv")(830)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case [_, "test"]:
            test()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
