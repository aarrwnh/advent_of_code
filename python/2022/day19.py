import math

from support import assert_result, read_file_lines, timing  # type: ignore

D = dict[str, int]
DD = dict[str, D]


def find_max_geode_robot(
    blueprint: DD,
    timeframe: int,
):
    curr_max_resources = {
        t: max(res.get(t, 0) for res in blueprint.values()) for t in blueprint.keys()
    }

    # [0, 0, 0, 0]
    resources = {t: 0 for t in blueprint}

    # [0, 0, 0, 1]
    robots = {t: 0 for t in blueprint}
    robots["ore"] = 1

    #  best_at: dict[int, int] = {}
    #  todo: list[tuple[int, ...]]
    #  todo = [(0, 1, 0, 0, 0, 0, 0, 0, 0)]

    queue: list[tuple[int, D, D, str | None]] = []
    queue.append((timeframe, resources, robots, None))
    geode_robots = 0

    while queue:
        time, resources, robots, prev_robot = queue.pop()

        if time == 0:
            geode_robots = max(geode_robots, resources["geode"])
            continue

        # this path can never beat our current maximum geode count
        if (
            geode_robots - resources["geode"]
            >= (time * (2 * robots["geode"] + time - 1)) // 2
        ):
            continue

        time -= 1
        wait = False

        for b_typ, res in blueprint.items():

            # if we already generate enough resources for this type
            # we don't need to create another robot to generate more
            if (
                b_typ != "geode"
                and robots[b_typ] * time + resources[b_typ]
                > curr_max_resources[b_typ] * time
            ):
                continue

            # don't create one of these if we could have created one last time
            if (prev_robot is None or prev_robot == b_typ) and all(
                v <= resources[t] - robots[t] for t, v in res.items()
            ):
                continue

            # we don't have enough resources to create a robot
            # if other robots did something, we could get enough resources, though
            if any(resources[t] < v for t, v in res.items()):
                wait = wait or all(robots[t] > 0 for t in res.keys())
                continue

            next_resources = {
                t: v + robots[t] - res.get(t, 0) for t, v in resources.items()
            }

            next_robots = {t: v + int(t == b_typ) for t, v in robots.items()}

            queue.append((time, next_resources, next_robots, b_typ))

        if wait:
            next_resources = {t: v + robots[t] for t, v in resources.items()}
            queue.append((time, next_resources, robots, None))

    return geode_robots


def parse_input(lines: list[str]):
    blueprints: dict[int, DD]
    blueprints = {}

    for line in lines:
        #  _id, o, c, o1, o2, g1, g2 = map(int, RE_BLUEPRINT.findall(line)[0])
        id_s, robots_s = line[10:-1].split(": ")

        id = int(id_s)
        blueprints[id] = {}

        # reverse because we want to go later from most -> least wanted robot
        for robot in reversed(robots_s.split(". ")):
            typ, costs = robot[5:].split(" robot costs ")
            blueprints[id][typ] = {
                resource_name: int(amount)
                for amount, resource_name in (
                    cost.split(" ") for cost in costs.split(" and ")
                )
            }

    return blueprints


@timing("part1")
def part1(lines: list[str]) -> int:
    blueprints = parse_input(lines)
    return sum([id * find_max_geode_robot(x, 24) for id, x in blueprints.items()])

    #  while todo:
    #      time, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo = todo.popleft()
    #      remaining = timeframe - time
    #      ore = min(blp.max_ore * remaining, ore)
    #      cla = min(blp.obsidian_robot.clay * remaining, cla)
    #      obs = min(blp.geode_robot.obsidian * remaining, obs)
    #      ore_b = min(ore_b, blp.max_ore)
    #      cla_b = min(cla_b, blp.obsidian_robot.clay)
    #      obs_b = min(obs_b, blp.geode_robot.obsidian)

    #  tup = (time, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo)
    #  if tup in seen:
    #      continue
    #  else:
    #      seen.add(tup)

    #  best_at[time] = max(best_at.get(time, 0), geo)

    #  if time == timeframe:
    #      continue


@timing("part2")
def part2(lines: list[str]) -> int:
    blueprints = parse_input(lines[:3])
    return math.prod([find_max_geode_robot(x, 32) for x in blueprints.values()])


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/19/sample.input")
    puzzle = read_file_lines(__file__, "../../input/2022/19/puzzle.input")

    assert_result(33, part1(sample))
    assert_result(960, part1(puzzle))

    assert_result(56 * 62, part2(sample))
    assert_result(2040, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Lagrange multiplier
