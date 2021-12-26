import re
from support import timing, check_result


@timing()
def compute(input: str):
    v = map(lambda x: int(x), re.findall(r"([-0-9]+)", input))
    xt1, xt2, yt1, yt2 = v

    max_y = 0
    path_count = 0

    #  sample = "target area: x=20..30, y=-10..-5"  # [5..14] [-4..9]
    #  puzzle = "target area: x=79..137, y=-176..-117"  # [13..69] [-87..175]
    for j in range(yt1, abs(yt1)):
        for start in range(5, xt2 + 1):
            path = [(0, 0), (start, j)]
            currentpath_max_y = 0
            while True:
                x, y = path[-1]

                if xt1 <= x <= xt2 and yt1 <= y <= yt2:
                    max_y = max(max_y, currentpath_max_y)
                    path_count += 1
                    break
                if x > xt2 or y < yt1:
                    break

                xd2, yd2 = path[-2]
                x_inc = x - xd2 - 1
                y_inc = y - yd2 - 1

                if x_inc > 0:
                    x += x_inc
                y += y_inc

                path.append((x, y))
                currentpath_max_y = max(currentpath_max_y, y)

    return [max_y, path_count]


def main() -> int:
    sample = "target area: x=20..30, y=-10..-5"  # [5..14] [-4..9]
    puzzle = "target area: x=79..137, y=-176..-117"  # [13..69] [-87..86,116..175]

    check_result([45, 112], compute(sample))
    check_result([15400, 5844], compute(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
