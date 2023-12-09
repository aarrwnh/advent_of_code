import re
from math import lcm

from support import InputReader, asserter, timing


class Map:
    instruct: str
    ins_size: int
    nodes: dict[str, tuple[str, str]]
    start_nodes: list[str]

    def __init__(self, lines: list[str]) -> None:
        nodes: dict[str, tuple[str, str]] = {}
        start_nodes: list[str] = []
        for line in lines[2:]:
            node, _, _, _, left, _, right, _ = re.split("[^\\w+]", line)
            nodes[node] = (left, right)
            # part2
            if node.endswith("A"):
                start_nodes.append(node)
        self.start_nodes = start_nodes
        self.nodes = nodes
        self.instruct = lines[0]
        self.ins_size = len(self.instruct)

    def walk(self, start_node: str, stop_node: str) -> int:
        count = 0
        n = self.nodes[start_node]

        while True:
            ins = self.instruct[count % self.ins_size]
            cand = n[1] if ins == "R" else n[0]
            if cand.endswith(stop_node):
                break
            n = self.nodes[cand]
            count += 1

        return count + 1


@asserter
@timing("part1")
def part1(map: Map) -> int:
    return map.walk("AAA", "ZZZ")


@asserter
@timing("part2")
def part2(map: Map) -> int:
    return lcm(*(map.walk(curr, "Z") for curr in map.start_nodes))


def main() -> int:
    i = InputReader(2023, 8)

    sample1 = Map(i.lines("sample"))
    sample2 = Map(i.lines("sample2"))
    sample3 = Map(i.lines("sample3"))
    puzzle = Map(i.lines("puzzle"))

    part1(sample1)(2)
    part1(sample2)(6)
    part1(puzzle)(22411)
    part2(sample3)(6)
    part2(puzzle)(11188774513823)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
