use std::collections::HashSet;

use utils::*;

fn main() {
    let input = InputReader::new("e2024", 2);
    check!(part1 <-    34 ; &input.load(1));
    check!(part2 <-  5191 ; &input.load(2));
    check!(part3 <- 11674 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    Runic::parse(&input).possible_words()
}
fn part2(input: &str) -> usize {
    Runic::parse(&input).possible_symbols()
}
fn part3(input: &str) -> usize {
    Runic::parse(&input).possible_scales()
}

#[derive(Debug)]
struct Runic<'a> {
    words: Vec<&'a str>,
    lines: Vec<&'a str>,
}

impl<'a> Runic<'a> {
    fn parse(input: &'a str) -> Self {
        if let Some((words, input)) = input.trim().split_once("\n\n") {
            Self {
                words: words
                    .strip_prefix("WORDS:")
                    .unwrap()
                    .split(',')
                    .collect::<Vec<_>>(),
                lines: input.split("\n").collect::<Vec<_>>(),
            }
        } else {
            unreachable!("input corrupted")
        }
    }

    fn possible_words(&self) -> usize {
        self.lines.iter().fold(0, |acc, line| {
            acc + (0..line.len())
                .map(|idx| {
                    self.words
                        .iter()
                        .filter(|x| line[idx..].starts_with(*x))
                        .count()
                })
                .sum::<usize>()
        })
    }

    fn possible_symbols(&self) -> usize {
        let mut count = 0;
        let mut p = vec![];
        for line in &self.lines {
            let width = line.len();
            p.resize(width, false);
            let rev = line.chars().rev().collect::<String>();
            for rune in &self.words {
                let len0 = rune.len();
                for idx in 0..width - len0 + 1 {
                    if line[idx..].starts_with(rune) {
                        for pos in idx..idx + len0 {
                            p[pos] = true;
                        }
                    }
                    if rev[idx..].starts_with(rune) {
                        for pos in idx..idx + len0 {
                            p[width - pos - 1] = true;
                        }
                    }
                }
            }
            count += p.iter().filter(|x| **x).count();
            p.clear();
        }
        count
    }

    fn possible_scales(&self) -> usize {
        let grid: Vec<char> = self
            .lines
            .iter()
            .flat_map(|line| line.chars().collect::<Vec<_>>())
            .collect();

        let height = self.lines.len() as i64;
        let width = self.lines.first().unwrap().len() as i64;

        let mut p = HashSet::new();
        let mut indices = vec![];

        for word in &self.words {
            let chars = word.chars().collect::<Vec<_>>();
            for row in 0..height {
                for col in 0..width {
                    'next: for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
                        indices.clear();
                        let mut r = row;
                        let mut c = col;

                        for ch in &chars {
                            if r < 0 || r >= height {
                                continue 'next;
                            }
                            let i = c + (r * width);
                            if *ch != grid[i as usize] {
                                continue 'next;
                            }
                            indices.push((r, c));
                            r += dir.0;
                            c += dir.1;
                            if c < 0 {
                                c = width - 1;
                            } else if c >= width {
                                c = 0;
                            }
                        }

                        for x in indices.drain(..) {
                            p.insert(x);
                        }
                    }
                }
            }
        }
        p.len()
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part1_example() {
        let input = r"
WORDS:THE,OWE,MES,ROD,HER

AWAKEN THE POWER ADORNED WITH THE FLAMES BRIGHT IRE";
        let r = Runic::parse(&input);
        assert_eq!(4, r.possible_words());
    }

    #[test]
    fn part2_example() {
        let input = "
WORDS:THE,OWE,MES,ROD,HER,QAQ

AWAKEN THE POWE ADORNED WITH THE FLAMES BRIGHT IRE
THE FLAME SHIELDED THE HEART OF THE KINGS
POWE PO WER P OWE R
THERE IS THE END
QAQAQ";
        let r = Runic::parse(&input);
        assert_eq!(42, r.possible_symbols());
    }

    #[test]
    fn part3_example() {
        let input = "
WORDS:THE,OWE,MES,ROD,RODEO

HELWORLT
ENIGWDXL
TRODEOAL";
        let r = Runic::parse(&input);
        assert_eq!(10, r.possible_scales());
    }
}
