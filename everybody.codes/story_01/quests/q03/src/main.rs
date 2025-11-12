use std::str::FromStr as _;

use utils::*;

fn main() {
    let input = InputReader::new("e1", 3);
    check!(part1 <-        3244 ; &input.load(1));
    check!(part2 <-     1011165 ; &input.load(2));
    check!(part3 <- 98303930565 ; &input.load(3));
}

fn part1(input: &str) -> u64 {
    input
        .trim()
        .lines()
        .map(|line| {
            let snail = Snail::from_str(line).unwrap();
            let end = snail.moves(100);
            end.0 + (100 * end.1)
        })
        .sum()
}

fn part2(input: &str) -> usize {
    golden_line(input)
    // loop {
    //     i += 1;
    //     let mut res = snails.iter().map(|snail| snail.advance(i));
    //     if res.all(|x| x == 0) {
    //         return i - 1;
    //     }
    // }
}

fn part3(input: &str) -> usize {
    golden_line(input)
}

fn golden_line(input: &str) -> usize {
    let mut n = Vec::new();
    let mut congruences = Vec::new();

    for line in input.trim().lines() {
        let Snail { pos, .. } = Snail::from_str(line).unwrap();
        n.push((pos.0 + pos.1) as i64 - 1);
        congruences.push(pos.1 as i64);
        // for i in 0..len {
        //     if (idx as i64 + i) % len == 0 {
        //         congruences.push(i as i64);
        //         break;
        //     }
        // }
    }

    chinese_remainder(n, congruences) as usize - 1
}

fn chinese_remainder(n: Vec<i64>, c: Vec<i64>) -> i64 {
    let mut sum = 0;
    let prod = n.iter().product::<i64>();
    for (n_i, c_i) in n.iter().zip(c.iter()) {
        let p = prod / n_i;
        sum += c_i * mul_inv(p, *n_i) * p;
    }
    sum % prod
}

fn mul_inv(mut a: i64, mut b: i64) -> i64 {
    let b0 = b;
    let mut x0 = 0;
    let mut x1 = 1;
    if b == 1 {
        return 1;
    }
    while a > 1 {
        let q = a / b;
        (a, b) = (b, a % b);
        (x0, x1) = (x1 - q * x0, x0);
    }
    if x1 < 0 {
        x1 += b0;
    }
    x1
}

type Point = (u64, u64);

#[derive(Debug)]
struct Snail {
    pos: Point,
    idx: usize,
    coords: Vec<Point>,
}

impl Snail {
    fn moves(self, days: usize) -> Point {
        self.coords[self.advance(days)]
    }

    fn advance(&self, days: usize) -> usize {
        (self.idx + days) % self.coords.len()
    }

    //   1234
    // 1 ...x
    // 2 ..x
    // 3 .p
    // 4 x
    fn gen_slope((x, y): Point) -> Vec<Point> {
        let mut arr = vec![(x, y)];
        Self::fill(&mut arr, (x - 1, y + 1), -1, 1); // left-downward
        arr.reverse();
        Self::fill(&mut arr, (x + 1, y - 1), 1, -1); // right-upward
        arr
    }

    fn fill(arr: &mut Vec<Point>, start: Point, dx: isize, dy: isize) {
        let mut x = start.0 as isize;
        let mut y = start.1 as isize;
        assert!(x >= 0 && y >= 0);
        while !(x < 1 || y < 1) {
            arr.push((x as u64, y as u64));
            x += dx;
            y += dy;
        }
    }

    fn u(s: &str) -> u64 {
        s.parse::<_>().unwrap()
    }
}

impl std::str::FromStr for Snail {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (x0, y0) = s.split_once(' ').unwrap();
        let pos = (Self::u(&x0[2..]), Self::u(&y0[2..]));

        let coords = Self::gen_slope(pos);
        let idx = coords.iter().position(|it| *it == pos).unwrap();

        Ok(Self { pos, idx, coords })
    }
}

#[cfg(test)]
mod q03 {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "
x=1 y=2
x=2 y=3
x=3 y=4
x=4 y=4";
        assert_eq!(1310, part1(input));
    }

    #[test]
    fn part2_example1() {
        let input = "
x=12 y=2
x=8 y=4
x=7 y=1
x=1 y=5
x=1 y=3";
        assert_eq!(14, part2(input));
    }

    #[test]
    fn part2_example2() {
        let input = "
x=3 y=1
x=3 y=9
x=1 y=5
x=4 y=10
x=5 y=3";
        assert_eq!(13659, part2(input));
    }
}
