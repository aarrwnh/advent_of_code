from support import timing

import day01
import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11
import day12
import day13
import day14


@timing()
def main() -> int:
    for i, m in enumerate(
        [
            day01,
            day02,
            day03,
            day04,
            day05,
            day06,
            day07,
            day08,
            day09,
            day10,
            day11,
            day12,
            day13,
            day14,
        ],
        1,
    ):
        print(f"\n  day {i: >2}")
        m.main()

    print("\n=== finished ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
