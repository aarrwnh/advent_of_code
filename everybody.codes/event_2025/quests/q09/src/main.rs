use std::{collections::HashMap, str::FromStr};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 9);
    check!(part1 <-   7310 ; &input.load(1));
    check!(part2 <- 317020 ; &input.load(2));
    check!(part3 <-  40329 ; &input.load(3));
}

fn part1(input: &str) -> u32 {
    let family = input.parse::<Family>().unwrap();
    family
        .combinations()
        .next()
        .map(|(p1, p2, ch)| family.get_score(p1, ch) * family.get_score(p2, ch))
        .into_iter()
        .sum()
}

fn part2(input: &str) -> u32 {
    let family = input.parse::<Family>().unwrap();
    family
        .combinations()
        .map(|(p1, p2, ch)| family.get_score(p1, ch) * family.get_score(p2, ch))
        .sum()
}

fn part3(input: &str) -> u32 {
    let family = input.parse::<Family>().unwrap();
    let mut edges: HashMap<usize, Vec<usize>> = HashMap::new();
    for (p1, p2, ch) in family.combinations() {
        edges.entry(ch).or_default().extend([p1, p2]);
        edges.entry(p1).or_default().push(ch);
        edges.entry(p2).or_default().push(ch);
    }
    family.find_largest(&edges)
}

struct Family {
    scales: Vec<(usize, [u128; 4])>,
}

impl FromStr for Family {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let scales = s
            .trim()
            .lines()
            .map(|line| line.split_once(':').unwrap())
            .map(|(a, b)| {
                let mut v = [0u128; 4];
                let b = b.as_bytes();
                for i in 0..128 {
                    let bc = match b[i] {
                        b'A' => 1,
                        b'C' => 2,
                        b'G' => 4,
                        b'T' => 8,
                        _ => unreachable!(),
                    };
                    v[i / 32] |= bc << ((i % 32) * 4);
                }
                (a.parse::<usize>().unwrap(), v)
            })
            .collect::<Vec<_>>();
        Ok(Self { scales })
    }
}

impl Family {
    fn get_score(&self, a: usize, b: usize) -> u32 {
        self.scales[a]
            .1
            .iter()
            .zip(self.scales[b].1.iter())
            .map(|(a, b)| (a & b).count_ones())
            .sum()
    }

    fn combinations(&self) -> Combinations<'_> {
        Combinations::new(&self.scales)
    }

    fn find_largest(&self, edges: &HashMap<usize, Vec<usize>>) -> u32 {
        let mut todo: Vec<usize> = Vec::new();
        let mut visited = vec![false; self.scales.len()];
        let mut best = vec![];
        let mut temp = vec![];
        for i in 0..self.scales.len() {
            if visited[i] {
                continue;
            }
            visited[i] = true;
            todo.push(i);
            temp.clear();
            temp.push(i);
            while let Some(curr) = todo.pop() {
                let Some(cand) = edges.get(&curr) else {
                    continue;
                };
                for &n in cand {
                    if visited[n] {
                        continue;
                    }
                    visited[n] = true;
                    todo.push(n);
                    temp.push(n);
                }
            }
            if temp.len() > best.len() {
                best = temp.clone();
            }
        }
        best.iter().map(|x| x + 1).sum::<usize>() as u32
    }
}

struct Combinations<'a> {
    scales: &'a Vec<(usize, [u128; 4])>,
    max_len: usize,
    p1: usize,
    p2: usize,
    ch: usize,
}

impl<'a> Combinations<'a> {
    fn new(scales: &'a Vec<(usize, [u128; 4])>) -> Self {
        Self {
            max_len: scales.len(),
            scales,
            p1: 0,
            p2: 1,
            ch: 0,
        }
    }
}

impl<'a> Iterator for Combinations<'a> {
    type Item = (usize, usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        let len = self.max_len;
        while self.p1 < len {
            if self.p2 < len {
                while self.ch < len {
                    let Self { p1, p2, ch, .. } = *self;
                    self.ch += 1;
                    if ch == p1 || ch == p2 {
                        continue;
                    }
                    if self.scales[p1]
                        .1
                        .iter()
                        .zip(self.scales[p2].1.iter())
                        .zip(self.scales[ch].1.iter())
                        .all(|((a, b), c)| ((a | b) & c) ^ c == 0)
                    {
                        return Some((p1, p2, ch));
                    }
                }
                self.p2 += 1;
                self.ch = 0;
            } else {
                self.p1 += 1;
                self.p2 = self.p1 + 1;
                self.ch = 0;
            }
        }

        None
    }
}

#[cfg(test)]
mod q09 {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "
1:CAAGCGCTAAGTTCGCTGGATGTGTGCCCGCG
2:CTTGAATTGGGCCGTTTACCTGGTTTAACCAT
3:CTAGCGCTGAGCTGGCTGCCTGGTTGACCGCG";
        assert_eq!(414, part1(input));
    }

    #[test]
    fn part2_example() {
        let input = "
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG";
        assert_eq!(1245, part2(input));
    }

    #[test]
    fn part3_example() {
        let input = "
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
8:GGCGTAAAGTATGGATGCTGGCTAGGCACCCG";
        assert_eq!(36, part3(input));
    }
}
