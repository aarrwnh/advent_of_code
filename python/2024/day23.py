import sys
from collections import defaultdict

from support import InputReader, asserter, timing


def parse(lines: list[str]) -> defaultdict[str, set[str]]:
    edges = defaultdict(set)
    for line in lines:
        a, b = line.split("-")
        edges[a].add(b)
        edges[b].add(a)
    return edges


@asserter
def part1(lines: list[str]) -> int:
    edges = parse(lines)
    visited: set[str] = set()
    connected: set[tuple[str, ...]] = set()

    for node in edges:
        paths = [[node, c] for c in edges[node]]
        for _ in range(2):
            n = []
            for path in paths:
                for dest in edges[path[-1]]:
                    if dest not in visited and dest != path[-2]:
                        n.append([*path, dest])
            paths = n

        visited.add(node)

        for path in paths:
            if path[0] == path[-1] and any(x for x in path[:-1] if x.startswith("t")):
                connected.add(tuple(sorted(path[:-1])))

    return len(connected)


@asserter
def part2(lines: list[str]) -> str:
    edges = parse(lines)
    cache: dict[tuple[str, ...], list[str]] = {}

    def find_largest(nodes: tuple[str, ...]) -> list[str]:
        if nodes in cache:
            return cache[nodes]

        cand: list[list[str]] = []
        for node in nodes:
            neighbors = edges[node] & set(nodes)
            if not neighbors:
                cand.append([node])
            else:
                n0 = [*find_largest(tuple(neighbors)), node]
                cand.append(sorted(n0))

        [*_, e] = sorted(cand, key=len)
        cache[nodes] = e
        return e

    return ",".join(find_largest(tuple(n for n in edges)))


@timing("day23")
def main() -> int:
    i = InputReader(2024, 23).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(7)
        assert part1(puzzle)(1348)

    def s2() -> None:
        assert part2(example)("co,de,ka,ta")
        assert part2(puzzle)("am,bv,ea,gh,is,iy,ml,nj,nl,no,om,tj,yv")

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
