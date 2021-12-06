from support import timing


#  def another_parse(fishes: str, days: int) -> int:
#      """https://www.twitch.tv/videos/1225522075"""
#      numbers = collections.Counter(int(s) for s in fishes.split(","))
#      for _ in range(days):
#          numbers2 = collections.Counter({6: numbers[0], 8: numbers[0]})
#          numbers2.update({k - 1: v for k, v in numbers.items() if k > 0})
#          #  for k, v in numbers.items():
#          #      if k > 0:
#          #          numbers2[k - 1] += v
#          numbers = numbers2
#      return sum(numbers.values())


def parse(fishes: str, days: int) -> int:
    tbl = [0] * 9
    for idx in fishes.split(","):
        tbl[int(idx)] += 1
    for day in range(days):
        tbl[(day + 7) % 9] += tbl[(day % 9)]
    return sum(tbl)


def check_result(expected: int, result: int) -> None:
    print(result == expected, f"{result} == {expected}")


@timing()
def main() -> int:
    sample = "3,4,3,1,2"
    puzzle = "3,3,2,1,4,1,1,2,3,1,1,2,1,2,1,1,1,1,1,1,4,1,1,5,2,1,1,2,1,1,1,3,5,1,5,5,1,1,1,1,3,1,1,3,2,1,1,1,1,1,1,4,1,1,1,1,1,1,1,4,1,3,3,1,1,3,1,3,1,2,1,3,1,1,4,1,2,4,4,5,1,1,1,1,1,1,4,1,5,1,1,5,1,1,3,3,1,3,2,5,2,4,1,4,1,2,4,5,1,1,5,1,1,1,4,1,1,5,2,1,1,5,1,1,1,5,1,1,1,1,1,3,1,5,3,2,1,1,2,2,1,2,1,1,5,1,1,4,5,1,4,3,1,1,1,1,1,1,5,1,1,1,5,2,1,1,1,5,1,1,1,4,4,2,1,1,1,1,1,1,1,3,1,1,4,4,1,4,1,1,5,3,1,1,1,5,2,2,4,2,1,1,3,1,5,5,1,1,1,4,1,5,1,1,1,4,3,3,3,1,3,1,5,1,4,2,1,1,5,1,1,1,5,5,1,1,2,1,1,1,3,1,1,1,2,3,1,2,2,3,1,3,1,1,4,1,1,2,1,1,1,1,3,5,1,1,2,1,1,1,4,1,1,1,1,1,2,4,1,1,5,3,1,1,1,2,2,2,1,5,1,3,5,3,1,1,4,1,1,4"

    check_result(26, parse(sample, days=18))
    check_result(5934, parse(sample, days=80))
    check_result(380758, parse(puzzle, days=80))

    check_result(26984457539, parse(sample, days=256))
    check_result(1710623015163, parse(puzzle, days=256))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
