use std::collections::HashSet;

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 8);
    check!(part1 <-      65 ; &input.load(1), 32);
    check!(part2 <- 2924486 ; &input.load(2), 256);
    check!(part3 <-    2795 ; &input.load(3), 256);
}

fn part1(input: &str, nails_count: isize) -> usize {
    let mid = (nails_count / 2) as isize;
    parse(input)
        .collect::<Vec<_>>()
        .windows(2)
        .map(|w| ((w[0] - w[1]).abs() == mid) as usize)
        .sum()
}

fn part2(input: &str, nails_count: isize) -> usize {
    let nails = parse(input).collect::<Vec<_>>();

    let mut total = 0;
    let mut lines: Vec<(isize, isize)> = Vec::new();

    for w in nails.windows(2) {
        let a = w[0].min(w[1]);
        let b = w[1].max(w[0]);

        for &(x, y) in &lines {
            if x == a || y == b {
                continue;
            }
            if (a > x && a < y) != (b > x && b < y) {
                total += 1;
            }
        }
        lines.push((a, b));
    }

    total
}

fn part3(input: &str, nails_count: isize) -> usize {
    let nails = parse(input).collect::<Vec<_>>();

    let mut max = 0;
    let lines: Vec<(isize, isize)> = nails
        .windows(2)
        .map(|w| match w {
            [a, b] => (*a.min(b), *b.max(a)),
            _ => panic!("invalid pair"),
        })
        .collect();

    let mid = (nails_count / 2) as isize;
    let mut tried = HashSet::new();
    for a0 in 1..=nails_count {
        for b0 in 1..=nails_count {
            let a = a0.min(b0);
            let b = b0.max(a0);
            if !tried.insert((a, b)) || a0 == b0 || b - a < mid {
                continue;
            }

            let mut sword_cuts = lines.contains(&(a, b)) as usize;
            for &(x, y) in &lines {
                if x == a || y == b {
                    continue;
                }
                if (a > x && a < y) != (b > x && b < y) {
                    sword_cuts += 1;
                }
            }

            max = max.max(sword_cuts);
        }
    }
    max
}

fn parse(input: &str) -> impl Iterator<Item = isize> {
    input.trim().split(',').map(|x| x.parse::<isize>().unwrap())
}

#[cfg(test)]
mod q08 {
    use super::*;

    #[test]
    fn part1_example() {
        assert_eq!(4, part1("1,5,2,6,8,4,1,7,3", 8));
    }

    #[test]
    fn part2_example() {
        assert_eq!(21, part2("1,5,2,6,8,4,1,7,3,5,7,8,2", 8));
    }

    #[test]
    fn part3_example() {
        assert_eq!(7, part3("1,5,2,6,8,4,1,7,3,6", 8));
    }
}
