import re

from support import check_result, read_file_lines, timing
from math import lcm


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

        return count


@timing("part1")
def part1(map: Map) -> int:
    return map.walk("AAA", "ZZZ") + 1


@timing("part2")
def part2(map: Map) -> int:
    total = 1
    for curr in map.start_nodes:
        total = lcm(total, map.walk(curr, "Z") + 1)

    return total


def main() -> int:
    sample = Map(read_file_lines("input/2023/08/sample"))
    sample2 = Map(read_file_lines("input/2023/08/sample2"))
    sample3 = Map(read_file_lines("input/2023/08/sample3"))
    puzzle = Map(read_file_lines("input/2023/08/puzzle"))

    check_result(2, part1(sample))
    check_result(6, part1(sample2))
    check_result(22411, part1(puzzle))

    check_result(6, part2(sample3))
    check_result(11188774513823, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
