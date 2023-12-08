from support import assert_result, read_file_lines, timing


def to_dec(p: str) -> int:
    match p:
        case "-":
            return -1
        case "=":
            return -2
        case _:
            return int(p)


def encode(n: int) -> str:
    ret = []
    while n:
        rem = n % 5
        ret.append(str(rem) if rem <= 2 else {3: "=", 4: "-"}[rem])
        n //= 5
        n += rem // 3
    return "".join(reversed(ret))


@timing("part1")
def part1(lines: list[str]) -> str:
    c = []
    for line in lines:
        c.append(sum([(to_dec(p) * 5**i) for i, p in enumerate(reversed(line))]))
    return encode(sum(c))


def main() -> int:
    sample = read_file_lines(__file__, "../../input/2022/25/sample")
    puzzle = read_file_lines(__file__, "../../input/2022/25/puzzle")

    assert_result("2=-1=0", part1(sample))
    assert_result("122-0==-=211==-2-200", part1(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#  REV = {
#      2: "2",
#      1: "1",
#      0: "0",
#      -1: "-",
#      -2: "=",
#  }
#  def z3encode(n: int) -> str:
#      from z3 import Int, Optimize, sat
#      near = int(math.log(n, 5))
#      for nterms in (near - 1, near, near + 1):
#          o = Optimize()
#          ints = []
#          for i in range(nterms):
#              this_int = Int(f"i_{i}")
#              o.add(this_int <= 2)
#              o.add(this_int >= -2)
#              ints.append(this_int * (5 ** (nterms - i - 1)))
#          o.add(sum(ints) == n)
#          if o.check() == sat:
#              m = o.model()
#              return "".join(REV[m[Int(f"i_{i}")].as_long()] for i in range(nterms))
#      raise AssertionError("unreachable")
