use std::collections::HashMap;

use utils::*;

fn main() {
    let input = InputReader::new("e2024", 5);
    check!(part1 <-             4322 ; &input.load(1));
    check!(part2 <-   15803440286010 ; &input.load(2));
    check!(part3 <- 9358100010021000 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    Dancer::from(input).part1(10)
}

fn part2(input: &str) -> usize {
    Dancer::from(input).part2_maybe_but_works()
}

fn part3(input: &str) -> usize {
    Dancer::from(input).part3()
}

struct Dancer {
    columns: Vec<Vec<usize>>,
}

struct DancerIter<'a> {
    dancer: &'a mut Dancer,
    round: usize,
    col: usize,
    /// round limit
    max_rounds: Option<usize>,
    /// collect shout after each round flag
    return_shout: Option<bool>,
}

impl DancerIter<'_> {
    fn get_column_mut(&mut self, index: usize) -> Option<&mut Vec<usize>> {
        self.dancer.columns.get_mut(index)
    }

    // fn shout(&mut self) -> usize {
    //     (0..self.dancer.width())
    //         .map(|c| self.get_column_mut(c).unwrap().first().unwrap().to_string())
    //         .collect::<String>() // join numbers
    //         .parse::<usize>() // convert to int
    //         .unwrap()
    // }

    fn shout(&mut self) -> usize {
        let mut num = 0;
        for b in (0..self.dancer.width()).filter_map(|c| self.get_column_mut(c)?.first().copied()) {
            let exp = (b as f32).log10() + 1.0;
            let p = 10_i32.pow(exp as u32) as usize;
            num = num * p + b;
        }
        num
    }
}

impl Iterator for DancerIter<'_> {
    type Item = (usize, Option<usize>);

    fn next(&mut self) -> Option<Self::Item> {
        if self.max_rounds.is_some_and(|r| self.round >= r) {
            return None;
        }

        let n_col = (self.col + 1) % self.dancer.width();
        let current = self.get_column_mut(self.col).unwrap().remove(0);
        match self.get_column_mut(n_col) {
            Some(column) => {
                let len = column.len();
                let dist = len * 2;
                let pos = (current - 1) % dist;
                let pos = if pos < len { pos } else { dist - pos };
                column.insert(pos, current);
            }
            None => panic!(),
        }

        self.col = n_col;
        self.round += 1;

        let shout = if self.return_shout.is_some()
            // part1: 10th round limit
            || self.max_rounds.is_some_and(|r| r == self.round)
        {
            Some(self.shout())
        } else {
            None
        };

        Some((self.round, shout))
    }
}

fn new_cache(columns: &[Vec<usize>]) -> Vec<usize> {
    const fn length(mut num: usize) -> usize {
        let mut len = 0;
        while num != 0 {
            num = num / 10;
            len += 1;
        }
        len
    }
    let nums = (0..columns.len())
        .map(|x| length(columns[x][0]))
        .sum::<usize>() as u32;
    vec![0usize; 10usize.pow(nums)]
}

impl Dancer {
    fn from(input: &str) -> Self {
        let lines = input.trim().lines().collect::<Vec<_>>();
        let spaces = lines[0].chars().filter(|x| *x == ' ').count();
        let mut columns = vec![Vec::new(); spaces + 1];
        for line in lines {
            for (col, num) in line.split(' ').enumerate() {
                columns[col].push(num.parse::<usize>().unwrap());
            }
        }
        Self { columns }
    }

    const fn width(&self) -> usize {
        self.columns.len()
    }

    fn iter(
        &'_ mut self,
        rounds: Option<usize>,
        return_shout: Option<bool>,
    ) -> impl Iterator<Item = (usize, Option<usize>)> + use<'_> {
        DancerIter {
            max_rounds: rounds,
            round: 0,
            col: 0,
            dancer: self,
            return_shout,
        }
    }

    fn part1(&mut self, rounds: usize) -> usize {
        for (_, shout) in self.iter(Some(rounds), None) {
            if let Some(shout) = shout {
                return shout;
            }
        }
        unreachable!()
    }

    fn part2_brute(&mut self) -> usize {
        let mut shouts = new_cache(&self.columns);
        let mut iter = self.iter(None, Some(true));
        while let Some((round, Some(result))) = iter.next() {
            shouts[result] += 1;
            if shouts[result] == 2024 {
                return round * result;
            }
        }
        unreachable!()
    }

    fn part3(&mut self) -> usize {
        let mut max = 0;
        let mut shouts = vec![];
        let mut iter = self.iter(None, Some(true));
        while let Some((_, Some(result))) = iter.next() {
            if shouts.contains(&result) && result == max {
                return result;
            }
            shouts.push(result);
            max = max.max(result);
        }
        unreachable!()
    }

    fn part2_maybe_but_works(&mut self) -> usize {
        let mut shouts = new_cache(&self.columns);
        let mut fingerprints: HashMap<usize, Vec<_>> = HashMap::new();

        // somehow guess next round number?
        let mut guesser = |round: usize, count: usize, result: usize| {
            let v = fingerprints.entry(result).or_default();
            v.push((count, round));
            let diffs = (0..v.len() - 1)
                .map(|i| {
                    let (a, b) = (v[i], v[i + 1]);
                    if b.0 - a.0 == 1 { b.1 - a.1 } else { panic!() } // + 1 ?
                })
                .collect::<Vec<_>>();
            if diffs.len() > 1 && diffs.len() % 2 == 0 {
                let mut prev_chunk = None;
                let chunks = diffs.len() / 2;
                for chunk in diffs.chunks(chunks) {
                    if prev_chunk.is_some_and(|y| y == chunk) {
                        let mut a0 = 0;
                        let mut a1 = 1 + chunks; // ??
                        let rem = chunk.iter().sum::<usize>();

                        // ??? 2023
                        if chunks == 1 {
                            a0 += (chunk[0] * 2023) - 1;
                            a1 = 0;
                        } else if chunks == 2 {
                            for (idx, diff) in chunk.iter().enumerate() {
                                a0 += (diff * 2023) / chunks;
                                a1 += v[v.len() - idx - 1].0; // + 1?
                            }
                        }

                        return Some(a0 + a1 + rem);
                    }
                    prev_chunk = Some(chunk);
                }
            }
            None
        };

        let mut prev_count = 1;
        let mut iter = self.iter(None, Some(true));
        while let Some((round, Some(result))) = iter.next() {
            let count = shouts[result];
            shouts[result] += 1;

            if prev_count == count {
                if let Some(v) = guesser(round, count, result) {
                    return v * result;
                }
                prev_count += 1;
            }

            // if prev_count == count && prev_count < 10 {
            //     println!(
            //         "{prev_round} -{} {round}  s:{result} {}",
            //         round - prev_round,
            //         shouts[result]
            //     );
            //     prev_count += 1;
            //     prev_round = round;
            // }
        }
        unreachable!()
    }

    // 0 0 -7 7  6285 2
    // 7 7 -4 11  6285 3
    // 11 11 -4 15  6285 4
    // 15 15 -4 19  6285 5
    // 19 19 -4 23  6285
    // 10 39 _8095_ 6285
    //
    //  | 8091 = (((round - prev_round) * 2023) - 1);
    //
    //  -------------
    //
    // 0    -79   79   12223436 2
    // 79   -1794 1873 11211915 3
    // 1873 -1658 3531 11101110 4
    //
    // 3531 -666 4197  11101110 5
    // 4197 -740 4937  11101110 6
    //
    // 4937 -666 5603  11101110 7
    // 5603 -740 6343  11101110 8
    //
    //  -------------
    //
    //  666 * 2024  = 1347984
    //  740 * 2024  = 1497760
    //  (666+740)/2 = 703
    //  (666+740)%2 = 0
    //  703 * 2024  = 1422872
    //
    //    ((666*2023)  +  (740*2023))  / 2             = 1422169
    //  ((((666*2023)) + ((740*2023))) / 2) - (-8-7-1) = 1422185 | 2022
    //
    //  1422185 | 2022
    //  1422851 | 2023
    //  1422851 + 740       = _1423591_
    //
    // 6343 -666 7009  11101110 8
    // 7009 -740 7749  11101110 10
    // 10 7749 _1423591_ 11101110
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "
2 3 4 5
3 4 5 2
4 5 2 3
5 2 3 4";
        assert_eq!(2323, Dancer::from(&input).part1(10));
    }

    #[test]
    fn part2_example() {
        let input = "
2 3 4 5
6 7 8 9";
        assert_eq!(50877075, Dancer::from(&input).part2_maybe_but_works());
    }

    #[test]
    fn part3_example() {
        let input = "
2 3 4 5
6 7 8 9";
        assert_eq!(6584, Dancer::from(&input).part3());
    }
}
