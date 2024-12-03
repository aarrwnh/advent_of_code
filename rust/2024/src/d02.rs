use std::str::FromStr;

use support::{check, InputReader};

fn is_safe(r: impl Iterator<Item = i64>) -> bool {
    let r = r.collect::<Vec<_>>();
    let dir = if r[1] < r[0] { -1 } else { 1 };
    r.windows(2)
        .all(|w| (1..=3).contains(&(dir * (w[1] - w[0]))))
}

fn parse_line(l: &str) -> impl Iterator<Item = i64> + '_ {
    l.split_whitespace().map(|x| i64::from_str(x).unwrap())
}

fn part1(input: &str) -> usize {
    input.lines().filter(|x| is_safe(parse_line(x))).count()
}

fn part2(input: &str) -> usize {
    input
        .lines()
        .filter(|x| {
            let r = parse_line(x).collect::<Vec<_>>();
            for i in 0..r.len() {
                let mut r = r.clone();
                r.remove(i);
                if is_safe(r.into_iter()) {
                    return true;
                }
            }
            false
        })
        .count()
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 2);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [2 &e] [606 &p]);
    check!("Part2" part2 [4 &e] [644 &p]);

    Ok(())
}
