use std::collections::HashMap;
use std::str::FromStr;

use support::{check, InputReader};

fn parse(input: &str) -> (Vec<u64>, Vec<u64>) {
    let mut a = Vec::new();
    let mut b = Vec::new();
    input.lines().for_each(|line| {
        let (left, right) = line.split_once("   ").unwrap();
        a.push(u64::from_str(left).unwrap());
        b.push(u64::from_str(right).unwrap());
    });
    (a, b)
}

fn part1(input: &str) -> u64 {
    let (mut left, mut right) = parse(input);
    left.sort();
    right.sort();
    left.iter().zip(right).map(|(a, b)| a.abs_diff(b)).sum()
}

fn part2(input: &str) -> u64 {
    let (left, right) = parse(input);
    let mut counter = HashMap::new();
    right.iter().for_each(|k| {
        counter.entry(k).and_modify(|v| *v += 1).or_insert(1);
    });
    left.iter().map(|k| *k * counter.get(k).unwrap_or(&0)).sum()
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 1);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [11 &e] [1579939 &p]);
    check!("Part2" part2 [31 &e] [20351745 &p]);

    Ok(())
}
