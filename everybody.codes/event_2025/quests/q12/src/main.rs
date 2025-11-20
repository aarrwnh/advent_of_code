use std::{collections::VecDeque, str::FromStr};

use rustc_hash::{FxHashMap, FxHashSet};
use utils::*;

fn main() {
    let input = InputReader::new("e2025", 12);
    check!(part1 <-  230 ; &input.load(1));
    check!(part2 <- 5753 ; &input.load(2));
    check!(part3 <- 4046 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    input
        .parse::<Experiment>()
        .unwrap()
        .ignite(&[((0, 0), 9)])
        .len()
}

fn part2(input: &str) -> usize {
    let b: Experiment = input.parse().unwrap();
    b.ignite(&[((0, 0), 9), ((b.max_col, b.max_row), 9)]).len()
}

fn part3(input: &str) -> usize {
    input.parse::<Experiment>().unwrap().find_greedy(3)
}

struct Experiment {
    barrels: FxHashMap<(isize, isize), usize>,
    max_col: isize,
    max_row: isize,
}

impl Experiment {
    const DIRS: [(isize, isize); 4] = [(-1, 0), (1, 0), (0, 1), (0, -1)];

    fn ignite(&self, fireballs: &[((isize, isize), usize)]) -> FxHashSet<(isize, isize)> {
        let mut seen: FxHashSet<_> = fireballs.iter().map(|&x| x.0).collect();
        let mut qu = VecDeque::from(fireballs.to_vec());

        while let Some(pos) = qu.pop_front() {
            let ((x, y), val) = pos;
            for (dx, dy) in Self::DIRS {
                let next = (x + dx, y + dy);
                if let Some(np) = self.barrels.get(&next)
                    && *np <= val
                    && seen.insert(next)
                {
                    qu.push_back((next, *np));
                }
            }
        }

        // println!();
        // for row in 0..=self.max_row {
        //     for col in 0..=self.max_col {
        //         if seen.contains(&(col as isize, row as isize)) {
        //             print!("#")
        //         } else {
        //             print!(".")
        //         }
        //     }
        //     println!()
        // }

        seen
    }

    // TODO: caching? / sets?
    fn find_greedy(&mut self, size: usize) -> usize {
        let mut fireballs = Vec::new();
        let mut ignited = FxHashSet::default();
        let mut best = FxHashMap::default();

        for _ in 0..size {
            best.clear();

            // remove prev visited from possible candidates
            self.barrels.retain(|pos, _| !ignited.contains(pos));

            for (&pos, &val) in &self.barrels {
                // TODO: remove manual trim
                if [3, 4, 5, 6, 9].contains(&val) {
                    let res = self.ignite(&[(pos, val)]);
                    best.insert(res.len(), (pos, val));
                }
            }

            fireballs.push(*best.iter().max().unwrap().1);
            ignited.extend(self.ignite(&fireballs));
        }

        ignited.len()
    }
}

impl FromStr for Experiment {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut grid = FxHashMap::default();
        let mut max_row = 0;
        let mut max_col = 0;
        for (row, line) in s.trim().lines().enumerate() {
            for (col, ch) in line.chars().enumerate() {
                grid.insert(
                    (col as isize, row as isize),
                    ch.to_digit(10).unwrap() as usize,
                );
                max_col = col as isize;
            }
            max_row = row as isize;
        }
        Ok(Self {
            barrels: grid,
            max_row,
            max_col,
        })
    }
}

#[cfg(test)]
mod q12 {
    use super::*;

    #[test]
    fn part1_example() {
        let s = "
989611
857782
746543
766789";
        assert_eq!(16, part1(s));
    }

    #[test]
    fn part2_example() {
        let s = "
9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859";
        assert_eq!(58, part2(s));
    }

    #[test]
    fn part3_example1() {
        let s = "
5411
3362
5235
3112";
        assert_eq!(14, part3(s));
    }

    #[test]
    fn part3_example2() {
        let s = "
41951111131882511179
32112222211508122215
31223333322105122219
31234444432147511128
91223333322176021892
60112222211166431583
04661111166111111746
01111119042122222177
41222108881233333219
71222127839122222196
56111026279711111507";
        assert_eq!(133, part3(s));
    }
}
