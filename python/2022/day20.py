from support import assert_result, read_file_int2, timing  # type: ignore


def shuffle(original: list[int], indices: list[int]):
    for i, n in enumerate(original):
        idx = indices.index(i)
        del indices[idx]
        new_idx = (idx + n) % len(indices)
        indices.insert(new_idx, i)
        #  print([original[n] for n in nums])


def decrypt(original: list[int], indices: list[int]):
    idx_0 = indices.index(original.index(0))
    return sum(
        original[indices[(idx_0 + i) % len(indices)]] for i in (1000, 2000, 3000)
    )


@timing("part1")
def part1(numbers: list[int]) -> int:
    indices = list(range(len(numbers)))
    shuffle(numbers, indices)
    return decrypt(numbers, indices)


@timing("part2")
def part2(numbers: list[int]) -> int:
    key = 811589153
    numbers = [x * key for x in numbers]
    indices = list(range(len(numbers)))
    for _ in range(10):
        shuffle(numbers, indices)
    return decrypt(numbers, indices)


def main() -> int:
    sample = read_file_int2(__file__, "../../input/2022/20/sample.input")
    puzzle = read_file_int2(__file__, "../../input/2022/20/puzzle.input")

    assert_result(3, part1(sample))
    assert_result(9687, part1(puzzle))

    assert_result(1623178306, part2(sample))
    assert_result(1338310513297, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
