use std::collections::{HashMap, HashSet, VecDeque};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 20);
    check!(part1 <- 126 ; &input.load(1));
    check!(part2 <- 579 ; &input.load(2));
    check!(part3 <- 458 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    let grid: Vec<Vec<char>> = input
        .trim()
        .lines()
        .map(|line| line.chars().filter(|&ch| ch != '.').collect())
        .collect();

    // for row in 0..grid.len() as i32 {
    //     for col in 0..grid[0].len() as i32 - 1 {
    //         if grid[row as usize][col as usize] == 'T' {
    //             for (nr, nc) in neighbours1(&(row as i32,col as i32)) {
    //                 if (row, col) < (nr, nc) && grid[nr as usize][nc as usize] == 'T' {
    //                     pairs += 1;
    //                 }
    //             }
    //         }
    //     }
    // }

    // check rows first
    let mut pairs = grid
        .iter()
        .map(|row| {
            row.windows(2)
                .filter(|w| w[0] == 'T' && w[0] == w[1])
                .count()
        })
        .sum();

    for (row, rest) in grid.iter().zip(&grid[1..]) {
        for (a, b) in row[1..].iter().step_by(2).zip(rest.iter().step_by(2)) {
            if *a == 'T' && a == b {
                pairs += 1;
            }
        }
    }
    pairs
}

fn part2(input: &str) -> usize {
    let mut start = (0, 0);
    let mut end = (0, 0);
    let mut grid: HashMap<(i32, i32), char> = HashMap::new();
    for (row, line) in input.trim().lines().enumerate() {
        for (col, ch) in line.chars().enumerate() {
            let p = (row as i32, col as i32);
            if ch != '.' {
                grid.insert(p, ch);
            }
            match ch {
                'S' => start = p,
                'E' => end = p,
                _ => {}
            }
        }
    }

    let mut seen = HashSet::from([start]);
    let mut qu = VecDeque::from([(0, start)]);

    while let Some((dist, pos)) = qu.pop_front() {
        if !grid.contains_key(&pos) {
            continue;
        }
        for n in neighbours1(pos) {
            if n == end {
                return dist + 1;
            }
            if seen.insert(n)
                && let Some(&ch) = grid.get(&n)
                && ch == 'T'
            {
                qu.push_back((dist + 1, n));
            }
        }
    }

    0
}

fn part3(input: &str) -> usize {
    let mut start = (0, 0);
    let mut end = (0, 0);
    let grid: Vec<Vec<char>> = input
        .trim()
        .lines()
        .enumerate()
        .map(|(row, line)| {
            line.chars()
                .filter(|ch| *ch != '.')
                .enumerate()
                .filter_map(|(col, ch)| {
                    let p = (row as i32, col as i32);
                    match ch {
                        'S' => start = p,
                        'E' => end = p,
                        _ => {}
                    }
                    Some(ch)
                })
                .collect()
        })
        .collect();

    let mut seen = HashSet::from([start]);
    let mut qu = VecDeque::from([(0, start)]);

    while let Some((dist, pos)) = qu.pop_front() {
        for n in neighbours2(pos, &grid) {
            if n == end {
                return dist + 1;
            }
            if seen.insert(n) && grid[n.0 as usize][n.1 as usize] == 'T' {
                qu.push_back((dist + 1, n));
            }
        }
    }

    0
}

fn neighbours1((r, c): (i32, i32)) -> impl Iterator<Item = (i32, i32)> {
    let a = if (c - r) % 2 == 0 { -1 } else { 1 };
    [(0, -1), (0, 1), (a, 0)]
        .into_iter()
        .map(move |(dr, dc)| (r + dr, c + dc))
}

const fn rotate(r: i32, c: i32, height: i32) -> (i32, i32) {
    // grid is rotating clockwise; our position ccw
    //
    // r | ----- c ----- |
    // c=0 -> r=3
    // c=1 -> r=2
    // c=2 -> r=2
    // c=4 -> r=1
    // c=5 -> r=1
    // c=6 -> r=0
    let a = height - i32::midpoint(c, 3) - r;
    let b = r * 2 + c % 2;
    (a, b)
}

fn neighbours2((r, c): (i32, i32), grid: &[Vec<char>]) -> Vec<(i32, i32)> {
    let mut res = Vec::with_capacity(5);

    let n = rotate(r, c, grid.len() as i32);
    res.push(n);

    let (nr, nc) = n;
    if nc > 0 {
        res.push((nr, nc - 1));
    }
    if nc < grid[nr as usize].len() as i32 - 1 {
        res.push((nr, nc + 1));
    }
    if nc % 2 == 0 {
        if nr > 0 {
            res.push((nr - 1, nc + 1));
        }
    } else {
        res.push((nr + 1, nc - 1));
    }
    res
}

#[cfg(test)]
mod q20 {
    use super::*;

    #[test]
    fn part1_example() {
        let s = "
T#TTT###T##
.##TT#TT##.
..T###T#T..
...##TT#...
....T##....
.....#.....";
        assert_eq!(7, part1(s));
    }

    #[test]
    fn part2_example() {
        let s = "
TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........";
        assert_eq!(32, part2(s));
    }

    #[test]
    fn part3_example() {
        let s = "
T####T#TTT##T##T#T#
.T#####TTTT##TTT##.
..TTTT#T###TTTT#T..
...T#TTT#ETTTT##...
....#TT##T#T##T....
.....#TT####T#.....
......T#TT#T#......
.......T#TTT.......
........TT#........
.........S.........";
        assert_eq!(23, part3(s));
    }
}
