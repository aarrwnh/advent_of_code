import collections
import itertools
import re
from typing import NamedTuple

from support import assert_result, read_file_lines, timing  # type: ignore

RE_LINE = re.compile(
    r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([\s,A-Z]+)"
)


class Valve(NamedTuple):
    name: int
    flow_rate: int
    adjacent: list[int]


def parse_input(lines: list[str]):
    valves: dict[int, Valve] = {}
    for line in lines:
        name_s, flow, child = RE_LINE.findall(line)[0]
        name = int.from_bytes(bytes(name_s, "utf-8"), byteorder="big")
        valves[name] = Valve(
            name,
            int(flow),
            [
                int.from_bytes(bytes(c, "utf-8"), byteorder="big")
                for c in child.split(", ")
            ],
        )
    return valves


# @timing("bfs")
def bfs(valves: dict[int, Valve], edges: list[int]):
    # find all possible paths
    weights: dict[tuple[int, ...], int] = {}
    for a, b in itertools.combinations(edges, r=2):
        todo_bfs: collections.deque[tuple[int, ...]] = collections.deque([(a,)])
        path: tuple[int, ...] = ()
        while todo_bfs:
            path = todo_bfs.popleft()
            if path[-1] == b:
                break
            else:
                possible_paths = [
                    (*path, n) for n in valves[path[-1]].adjacent if n not in path
                ]
                todo_bfs.extend(possible_paths)

        weights[(a, b)] = len(path)
        weights[(b, a)] = len(path)

    return weights


AA = int.from_bytes(b"AA", byteorder="big")


def calculate_routes_costs(valves: dict[int, Valve], timelimit: int = 30):
    have_positive_flow = frozenset(k for k, v in valves.items() if v.flow_rate > 0)
    edges = [AA, *have_positive_flow]

    weights = bfs(valves, edges)

    # time to total
    best: dict[frozenset[int], int] = {}
    todo: list[tuple[int, int, int, frozenset[int]]]
    todo = [(0, 0, AA, frozenset())]

    while todo:
        score, time, current, seen = todo.pop()

        best[seen] = max(best.get(seen, score), score)
        #  route_k = frozenset(current) - {AA}
        #  best_val = best.setdefault(route_k, score)
        #  best[route_k] = max(best_val, score)

        for p in have_positive_flow - seen:
            needed_time = time + weights[(current, p)]
            if needed_time < timelimit:
                todo.append(
                    (
                        score + (timelimit - needed_time) * valves[p].flow_rate,
                        needed_time,
                        # route + (p,),
                        p,
                        # seen - {p},
                        seen | {p},
                    )
                )

    return best


@timing("part1")
def part1(valves: dict[int, Valve]) -> int:
    best = calculate_routes_costs(valves, 30)
    return max(best.values())


@timing("part2")
def part2(valves: dict[int, Valve]) -> int:
    best = calculate_routes_costs(valves, 26)
    return max(
        best[k1] + best[k2]
        for k1, k2 in itertools.combinations(best, r=2)
        if not k1 & k2
    )


def main() -> int:
    sample = parse_input(read_file_lines(__file__, "../../input/2022/16/sample.input"))
    puzzle = parse_input(read_file_lines(__file__, "../../input/2022/16/puzzle.input"))

    assert_result(1651, part1(sample))
    assert_result(1376, part1(puzzle))

    assert_result(1707, part2(sample))
    assert_result(1933, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
