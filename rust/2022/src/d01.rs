use std::{collections::BinaryHeap, error::Error, fs::read_to_string, str::FromStr};
use support::*;

#[derive(Debug)]
struct Input(Vec<Vec<u32>>);

impl FromStr for Input {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self(
            s.split("\n\n")
                .map(|chunk| chunk.lines().flat_map(u32::from_str).collect::<Vec<_>>())
                .collect::<Vec<_>>(),
        ))
    }
}

fn get_calories(chunks: &[Vec<u32>]) -> impl Iterator<Item = u32> + '_ {
    chunks.iter().map(|invertory| invertory.iter().sum::<u32>())
}

fn part1(input: &str) -> u32 {
    let i = Input::from_str(input).expect("");
    get_calories(&i.0).max().unwrap()
}

fn part2(input: &str) -> u32 {
    let i = Input::from_str(input).expect("");
    // calories.sort_by(|a, b| b.cmp(a));
    get_calories(&i.0)
        .collect::<BinaryHeap<_>>()
        .iter()
        .take(3)
        .sum()
}

pub fn main() -> Result<(), Box<dyn Error>> {
    let i = InputReader::new(2022, 1);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [24000 &e] [71924 &p]);
    check!("Part2" part2 [45000 &e] [210406 &p]);

    Ok(())
}
