import heapq
import itertools
import sys
from collections import defaultdict, deque

from support import InputReader, asserter, timing

Graph = defaultdict[str, dict[str, int]]


def find_shortest(graph: Graph, start: str) -> int:
    queue: list[tuple[int, tuple[str, ...]]] = [(0, (start,))]

    while queue:
        current_distance, path = heapq.heappop(queue)

        if len(path) == len(graph):
            return current_distance

        for n, dist in graph[path[-1]].items():
            if n not in path:
                distance = current_distance + dist
                heapq.heappush(queue, (distance, (*path, n)))

    raise AssertionError("unreachable")


def find_longest(graph: Graph) -> int:
    a = [(0, (start,)) for start in graph]
    queue: deque[tuple[int, tuple[str, ...]]] = deque(a)
    longest = 0
    size = len(graph)

    distances = {k: 0 for k in graph}

    while queue:
        current_distance, path = queue.pop()

        if len(path) == size:
            longest = max(longest, current_distance)
        else:
            if current_distance > distances[path[-1]]:
                continue
            for n, dist in graph[path[-1]].items():
                distance = current_distance + dist
                if n not in path:
                    queue.append((distance, (*path, n)))
                    distances[n] = distance

    return longest


def parse(lines: list[str]) -> Graph:
    graph: Graph = defaultdict(dict)
    for line in lines:
        src, _, dest, _, dist_s = line.split(" ")
        graph[src][dest] = graph[dest][src] = int(dist_s)
    return graph


def find_all(graph: Graph) -> list[int]:
    return [
        sum(graph[src][dst] for src, dst in itertools.pairwise(perm))
        for perm in itertools.permutations(graph.keys())
    ]


@asserter
def part1(lines: list[str]) -> int:
    graph = parse(lines)
    return min(find_shortest(graph, start) for start in graph)


@asserter
def part2(lines: list[str]) -> int:
    return max(find_all(parse(lines)))
    # return find_longest(parse(lines))


@timing("day9")
def main() -> int:
    i = InputReader(2015, 9).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example)(605)
        assert part1(puzzle)(207)

    def s2() -> None:
        assert part2(example)(982)
        assert part2(puzzle)(804)

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
