from support import assert_result, read_file_lines, timing  # type: ignore

SPACE_AVAILABLE = 70000000
SPACE_NEEDED = 30000000


def get_tree(lines: list[str]) -> tuple[int, dict[str, int]]:
    tree = {"/": 0}
    path: list[str] = []
    current_dir = "/"
    total = 0

    for line in lines:
        # handle command
        if line.startswith("$"):
            if line == "$ ls":
                pass
            elif line == "$ cd ..":
                path.pop()
            else:
                _, _, dirname = line.split(" ", 2)
                path.append(dirname)
                current_dir = "/".join(path)
                tree.setdefault(current_dir, 0)

        # create dir
        elif line.startswith("dir"):
            pass

        # create file
        else:
            size, _ = line.split(" ", 1)
            tree[current_dir] += int(size)
            total += int(size)

    return total, tree


@timing()
def part1(lines: list[str]) -> int:
    _, tree = get_tree(lines)
    #  tree.pop("/")

    def count(path: str) -> int:
        total = 0
        for k, v in tree.items():
            if k.startswith(path):
                total += v

        if total > 100000:
            return 0
        else:
            return total

    return sum([count(dir) for dir in tree.keys()])


@timing()
def part2(lines: list[str]) -> int:
    total, tree = get_tree(lines)
    space_unsued = SPACE_AVAILABLE - total

    def count(path: str) -> int:
        total = 0
        for k, v in tree.items():
            if k.startswith(path):
                total += v
        return total

    for size in sorted([count(dir) for dir in tree.keys()]):
        if space_unsued + size > SPACE_NEEDED:
            return size

    raise AssertionError("")


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/07/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/07/puzzle.input")

    assert_result(95437, part1(sample))
    assert_result(1648397, part1(puzzle))

    assert_result(24933642, part2(sample))
    assert_result(1815525, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
