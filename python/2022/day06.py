from support import check_result, read_file_raw, timing  # type: ignore


def read_signal(signal: str, start: int) -> int:
    idx = 0
    size = len(signal)
    while True:
        if idx == size - 1:
            break
        chunk = signal[idx : idx + start]
        if len(set(chunk)) == start:
            break
        idx = idx + 1
    return idx + start


#  def read_signal(signal: str, start: int) -> int:
#      idx = 0
#      queue: list[str] = []
#      while True:
#          char = signal[idx]
#          queue.insert(0, char)
#          idx = idx + 1
#          if len(queue) > start:
#              queue.pop()
#              if len(set(queue)) == start:
#                  return idx

#  def read_signal(signal: str, start: int) -> int:
#      d: deque[str] = deque(maxlen=start)
#      for i, c in enumerate(signal.strip()):
#          d.append(c)
#          if len(d) == start and len(set(d)) == start:
#              return i + 1
#      raise NotImplementedError("!")


@timing()
def part1(signal: str) -> int:
    return read_signal(signal, 4)


@timing()
def part2(signal: str) -> int:
    return read_signal(signal, 14)


def main() -> int:
    sample = read_file_raw(__file__, "../../input/2022/06/sample.input")
    puzzle = read_file_raw(__file__, "../../input/2022/06/puzzle.input")

    check_result(7, part1(sample))
    check_result(5, part1("bvwbjplbgvbhsrlpgdmjqwftvncz"))
    check_result(6, part1("nppdvjthqldpwncqszvftbrmjlhg"))
    check_result(10, part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"))
    check_result(11, part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"))
    check_result(1093, part1(puzzle))

    check_result(19, part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb"))
    check_result(3534, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
