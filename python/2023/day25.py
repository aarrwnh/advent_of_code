import sys
from collections import Counter, defaultdict, deque

from support import InputReader, asserter, timing


class Wires:
    def __init__(self, lines: list[str]) -> None:
        self.edges: Counter[tuple[str, str]] = Counter()
        self.nodes: defaultdict[str, list[str]] = defaultdict(list)

        for line in lines:
            left, right_s = line.split(": ")
            right = right_s.split(" ")
            for c in right:
                self.nodes[left].append(c)
                self.nodes[c].append(left)

    def find_one(self) -> tuple[str, str]:
        for src in self.nodes:  # count nodes
            self._walk_nodes(src, count=True)
        edge = self._remove_max()
        self._remove_edge(edge)
        return edge

    def _remove_max(self) -> tuple[str, str]:
        max_v = 0
        max_edge = ("", "")
        for k in self.edges:
            v = self.edges[k]
            if v > max_v:
                max_v = v
                max_edge = k
        del self.edges[max_edge]
        return max_edge

    def _walk_nodes(self, start: str, *, count: bool = True) -> int:
        visited = set()
        queue = deque([start])

        while queue:
            src = queue.popleft()
            for dest in self.nodes[src]:
                if dest in visited:
                    continue
                queue.append(dest)
                visited.add(dest)

                if count:
                    if src < dest:
                        self.edges[(src, dest)] += 1
                    else:
                        self.edges[(dest, src)] += 1

        return len(visited)

    def count_nodes(self, start: str) -> int:
        return self._walk_nodes(start)

    def _remove_edge(self, edge: tuple[str, str]) -> None:
        src, dest = edge

        new_edge: set[str] = set()
        for val in self.nodes[src]:
            if val != dest:
                new_edge.add(val)
        self.nodes[src] = list(new_edge)

        new_edge = set()
        for val in self.nodes[dest]:
            if val != src:
                new_edge.add(val)
        self.nodes[dest] = list(new_edge)


# def _connected_components(nodes: dict[str, set[str]]) -> list[int]:
#     ret = []
#     while nodes:
#         done = set()
#         node = next(iter(nodes))
#         processing = [node]
#         while processing:
#             node = processing.pop()
#             for other in nodes[node]:
#                 processing.append(other)
#                 nodes[other].remove(node)
#             del nodes[node]
#             done.add(node)
#         ret.append(len(done))
#     return ret


@asserter
@timing("part1")
def part1(lines: list[str]) -> float:
    w = Wires(lines)
    samples = [w.find_one() for _ in range(3)]
    return w.count_nodes(samples[0][0]) * w.count_nodes(samples[0][1])

    # connections = list(comp)
    # for i, c1 in enumerate(connections):
    #     for j, c2 in enumerate(connections[i + 1 :], start=i + 1):
    #         for c3 in connections[j + 1 :]:
    #             cand = copy.deepcopy(nodes)
    #             for src, dest in (c1, c2, c3):
    #                 cand[src].remove(dest)
    #                 cand[dest].remove(src)
    #             components = _connected_components(cand)
    #             if len(components) == 2:
    #                 return math.prod(components)


def main() -> int:
    i = InputReader(2023, 25).lines

    sample = i("sample")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(sample)(54)
        assert part1(puzzle)(600369)

    match sys.argv:
        case _:
            s1()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
