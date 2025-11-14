use utils::*;

fn main() {
    let input = InputReader::new("e2025", 8);
    check!(part1 <-      65 ; &input.load(1), 32);
    check!(part2 <- 2924486 ; &input.load(2), 256);
    check!(part3 <-    2795 ; &input.load(3), 256);
}

fn part1(input: &str, nails_count: usize) -> usize {
    let mid = nails_count / 2;
    parse(input)
        .iter()
        .map(|(a, b)| (b - a == mid) as usize)
        .sum()
}

fn part2(input: &str, nails_count: isize) -> usize {
    let mut total = 0;
    let mut strings: Vec<(usize, usize)> = Vec::new();

    for (a, b) in parse(input) {
        for &(x, y) in &strings {
            if x == a || y == b {
                continue;
            }
            if (a > x && a < y) != (b > x && b < y) {
                total += 1;
            }
        }
        strings.push((a, b));
    }

    total
}

fn part3(input: &str, nails_count: usize) -> usize {
    // let mut max = 0;
    // let mid = (nails_count / 2) as isize;
    // let mut tried = HashSet::new();
    // for a0 in 1..=nails_count {
    //     for b0 in 1..=nails_count {
    //         let a = a0.min(b0);
    //         let b = b0.max(a0);
    //         if !tried.insert((a, b)) || a0 == b0 || b - a < mid {
    //             continue;
    //         }
    //         let mut sword_cuts = lines.contains(&(a, b)) as usize;
    //         for &(x, y) in &lines {
    //             if x == a || y == b {
    //                 continue;
    //             }
    //             if (a > x && a < y) != (b > x && b < y) {
    //                 sword_cuts += 1;
    //             }
    //         }
    //         max = max.max(sword_cuts);
    //     }
    // }

    let n = nails_count;
    let mut map = vec![vec![0usize; n]; n];

    let mut update = |r1: usize, c1: usize, r2: usize, c2: usize| {
        if r1 < 1 || c1 < 1 || r1 > n || c1 > nails_count {
            return;
        }

        map[r1 - 1][c1 - 1] += 1;
        if c2 < n {
            map[r1 - 1][c2] -= 1;
        }
        if r2 < n {
            map[r2][c1 - 1] -= 1;
        }
        if c2 < n && n > r2 {
            map[r2][c2] += 1;
        }
    };

    for (a, b) in parse(input) {
        update(a + 1, b + 1, b - 1, n);
        update(1, a + 1, a - 1, b - 1);
        update(a, b, a, b);
    }

    for r in 1..n {
        for c in 0..n {
            map[r][c] += map[r - 1][c];
        }
    }

    for r in 0..n {
        for c in 1..n {
            map[r][c] += map[r][c - 1];
        }
    }

    *map.iter().map(|x| x.iter().max().unwrap()).max().unwrap()
}

fn parse(input: &str) -> Vec<(usize, usize)> {
    let nails = input
        .trim()
        .split(',')
        .map(|x| x.parse::<usize>().unwrap())
        .collect::<Vec<_>>();
    nails
        .windows(2)
        .map(|w| match w {
            [a, b] => (*a.min(b), *b.max(a)),
            _ => panic!("invalid pair"),
        })
        .collect::<Vec<_>>()
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
