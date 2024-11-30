use array_tool::vec::*;
use std::{
    collections::{HashMap, HashSet},
    error::Error,
    fs::read_to_string,
    io::{self, ErrorKind},
    // mem::take,
    string::ParseError,
    time::SystemTime,
};
use support::{check, InputReader};

const LOWERCASE_ITEM: u32 = 'a' as u32 - 1; // + 1;
const UPPERCASE_ITEM: u32 = 'A' as u32 - 27; // + 27;

#[derive(Debug, PartialEq)]
struct Item {
    value: usize,
}

impl TryFrom<&u8> for Item {
    type Error = ();

    fn try_from(value: &u8) -> Result<Self, Self::Error> {
        let value = if *value > b'a' {
            *value - b'a' + 1
        } else {
            *value - b'A' + 27
        };

        Ok(Self {
            value: value as usize,
        })
    }
}

fn part1_by_cod3monk(input: &Vec<&str>) -> usize {
    let mut sum = 0usize;

    for values in input {
        let (part1, part2) = values.as_bytes().split_at(values.len() / 2);

        let mut occurences: [bool; 53] = [false; 53];
        for x in part1 {
            let item = Item::try_from(x).unwrap();
            occurences[item.value] = true;
        }

        for x in part2 {
            let item = Item::try_from(x).unwrap();
            if occurences[item.value] {
                sum += item.value;
                break;
            }
        }
    }
    sum
}

fn part2_by_cod3monk(input: &[&str]) -> usize {
    input.chunks(3).map(check_group).sum()
}

fn check_group(chunk: &[&str]) -> usize {
    let mut occurences: [u8; 53] = [0; 53];
    let mut sum = 0;

    for (row_index, sack) in chunk.iter().enumerate() {
        for element in sack.as_bytes() {
            let item = Item::try_from(element).unwrap();

            if row_index < 2 {
                // On the two first rows we mark the element on the occurences
                occurences[item.value] |= 1 << row_index;
            } else if occurences[item.value] == 0b011 {
                // on the thrid row we check if the two contains the element
                sum += item.value;
                break;
            }
        }
    }
    sum
}

/// average: 742 µs
fn part2(input: &[&str]) -> u32 {
    let mut total = 0;
    for idx in (0..input.len()).step_by(3) {
        let group = &input[idx..idx + 3];
        let g1 = group.first().unwrap();
        let g2 = group.get(1).unwrap();
        let g3 = group.get(2).unwrap();
        for c in g1.chars() {
            let m2 = g2.matches(c);
            let a2 = m2.collect::<Vec<&str>>();
            if a2.is_empty() {
                continue;
            }
            let m3 = g3.matches(c);
            let a3 = m3.collect::<Vec<&str>>();
            if !a3.is_empty() {
                let w = c as u32;
                let ord = match c.is_uppercase() {
                    true => w - 38,
                    false => w - 96,
                };
                total += ord;
                break;
            }
        }
    }
    total
}

fn part1_p(input: &[&str]) -> u32 {
    input
        .iter()
        .map(|line| {
            let (a, b) = line.split_at(line.len() / 2);
            let a = a.chars().collect::<HashSet<char>>();

            b.chars()
                .filter(move |char| a.contains(char))
                .map(|char| {
                    if char.is_lowercase() {
                        char as u32 - LOWERCASE_ITEM
                    } else {
                        char as u32 - UPPERCASE_ITEM
                    }
                })
                .last()
                .unwrap()
        })
        .sum::<u32>()
}

fn part1_slow(input: &Vec<&str>) -> u32 {
    let mut total = 0;
    for line in input {
        let (a, b) = line.split_at(line.len() / 2);
        let c = [a, b].map(|s| s.chars().collect::<HashSet<char>>());
        let shared_char: HashSet<_> = c[0].intersection(&c[1]).collect();
        for &char in shared_char {
            total += if char.is_lowercase() {
                char as u32 - LOWERCASE_ITEM
            } else {
                char as u32 - UPPERCASE_ITEM
            };
        }
    }
    total
}

/// adapted from ThePrimeagen
/// this is horrendously slow > 12272 µs
fn part2_theprimeagen(input: &[&str]) -> u32 {
    let mut total = 0;
    for chunk in input.chunks(3) {
        let c = chunk
            .iter()
            .flat_map(|l| l.chars().collect::<HashSet<_>>().into_iter())
            .fold(HashMap::new(), |mut h: HashMap<char, u32>, x| {
                *h.entry(x).or_insert(0) += 1;
                h
            })
            .into_iter()
            .filter(|(_, v)| *v == 3)
            .last();

        if let Some((char, _)) = c {
            total += if char.is_lowercase() {
                char as u32 - LOWERCASE_ITEM
            } else {
                char as u32 - UPPERCASE_ITEM
            };
        }
    }
    total
}

fn part1_fast(input: &Vec<&str>) -> u32 {
    let mut total = 0;
    for line in input {
        let half = line.len() / 2;
        let right = line.get(half..).unwrap();
        let left = line.get(..half).unwrap();
        for c in left.chars() {
            let m = right.matches(c);
            let a = m.collect::<Vec<&str>>();
            if !a.is_empty() {
                let w = c as u32;
                let ord = match c.is_uppercase() {
                    true => w - 38,
                    false => w - 96,
                };
                total += ord;
                break;
            }
        }
    }
    total
}

fn part2_2(input: &[&str]) -> u32 {
    let mut total = 0;
    let chunks = input.chunks(3);
    for chunk in chunks {
        let g1 = chunk[0].split("").collect::<Vec<&str>>();
        let g2 = chunk[1].split("").collect::<Vec<&str>>();
        let g3 = chunk[2].split("").collect::<Vec<&str>>();
        let common_val = g1.intersect(g2.intersect(g3))[1];
        let w: char = common_val.chars().collect::<Vec<char>>()[0];
        let c = w as u32;
        total += if w.is_lowercase() {
            c - LOWERCASE_ITEM
        } else {
            c - UPPERCASE_ITEM
        };
    }
    total
}
pub fn main() -> Result<(), Box<dyn Error>> {
    let i = InputReader::new(2022, 3);
    let e = i.as_raw("example");
    let p = i.as_raw("puzzle");
    let e = e.lines().collect::<Vec<&str>>();
    let p = p.lines().collect::<Vec<&str>>();

    check!("Part1" part1_by_cod3monk [157 &e] [7908 &p]);
    check!("Part2" part2_by_cod3monk [70 &e] [2838 &p]);

    check!("Part1_slow" part1_slow [157 &e] [7908 &p]);
    check!("Part2_slow" part2_2 [70 &e] [2838 &p]);

    // print!("\n  part1_fast\n");
    // check_values!(157, part1_fast, &sample);
    // check_values!(7908, part1_fast, &puzzle);

    // print!("\n  part1_slow\n");
    // check_values!(157, part1_slow, &sample, true);
    // check_values!(7908, part1_slow, &puzzle, true);

    // print!("\n  part1_p\n");
    // check_values!(157, part1_p, &sample, true);
    // check_values!(7908, part1_p, &puzzle, true);

    // print!("\n  part2\n");
    // check_values!(70, part2, &sample);
    // check_values!(2838, part2, &puzzle);

    // print!("\n  part2_theprimeagen\n");
    // check_values!(70, part2_theprimeagen, &sample, true);
    // check_values!(2838, part2_theprimeagen, &puzzle, true);

    // print!("\n  part1_by_cod3monk\n");
    // check_values!(157, part1_by_cod3monk, &sample, true);
    // check_values!(7908, part1_by_cod3monk, &puzzle, true);

    // print!("\n  part2_by_cod3monk\n");
    // check_values!(157, part2_by_cod3monk, &sample, true);
    // check_values!(7908, part2_by_cod3monk, &puzzle, true);

    // print!("\n  part2_2\n");
    // check_values!(70, part2_2, &sample, true);
    // check_values!(2838, part2_2, &puzzle, true);

    Ok(())
}
