import sys

from support import InputReader, asserter, timing


@asserter
def part1(lines: list[str], timelimit: int) -> int:
    results: set[int] = set()
    for line in lines:
        a = line.split()
        speed, duration, rest = int(a[3]), int(a[6]), int(a[13])

        elapsed = 1
        distance = 0

        while elapsed < timelimit:
            elapsed += duration
            if elapsed >= timelimit:
                break
            else:
                distance += speed * duration
            elapsed += rest
        results.add(distance)

    return max(results)


class Deer:
    def __init__(self, speed: int, duration: int, rest: int) -> None:
        self.speed = speed
        self.duration = duration
        self.rest = rest

        self.score = 0
        self.distance = 0
        self.flying = True
        self.cooldown = self.duration

    def tick(self) -> int:
        if self.flying:
            self.distance += self.speed

        self.cooldown -= 1

        if self.cooldown == 0:
            self.flying = not self.flying
            self.cooldown = self.duration if self.flying else self.rest

        return self.distance

    def add_point(self, top: int) -> None:
        if self.distance == top:
            self.score += 1

    def __repr__(self) -> str:
        return f"{self.distance} {self.score}"


@asserter
def part2(lines: list[str], timelimit: int) -> int:
    deers: list[Deer] = []
    for line in lines:
        a = line.split()
        speed, per, rest = int(a[3]), int(a[6]), int(a[13])
        deers.append(Deer(speed, per, rest))

    for _ in range(timelimit):
        top = max(deer.tick() for deer in deers)
        for deer in deers:
            deer.add_point(top)

    return max(deer.score for deer in deers)


@timing("day14")
def main() -> int:
    i = InputReader(2015, 14).lines

    example = i("example")
    puzzle = i("puzzle")

    def s1() -> None:
        assert part1(example, 1000)(1120)
        assert part1(puzzle, 2503)(2655)

    def s2() -> None:
        assert part2(example, 1000)(689)
        assert part2(puzzle, 2503)(1059)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
