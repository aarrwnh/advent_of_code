use std::{
    collections::HashMap,
    sync::{LazyLock, Mutex, OnceLock},
};

use support::{check, InputReader};

trait Stone<T> {
    fn split(self) -> Vec<T>;
}

// static CACHE: LazyLock<Mutex<HashMap<usize, Vec<usize>>>> =
//     LazyLock::new(|| Mutex::new(HashMap::new()));

impl Stone<usize> for usize {
    fn split(self) -> Vec<Self> {
        if self == 0 {
            return vec![1];
        }

        let mut v = Vec::new();
        let f = (self as u64).ilog10();
        if f % 2 == 1 {
            let mut div = 10;
            while (self / div) > div {
                div *= 10;
            }
            v.extend([self / div, self % div]);
        } else {
            v.push(self * 2024);
        }
        v
    }
}

fn blinker(input: &str, blinks: usize) -> usize {
    let mut cache = HashMap::new();
    let mut ct = input
        .split_whitespace()
        .map(|stone| (stone.parse::<usize>().unwrap(), 1))
        .collect::<HashMap<usize, usize>>();
    for _ in (0..blinks) {
        let mut next = HashMap::new();
        for (stone, count) in ct {
            let stones = match cache.get(&stone) {
                Some(prev) => prev,
                None => cache.entry(stone).or_insert(stone.split()),
            };
            for new_stone in stones {
                *next.entry(*new_stone).or_default() += count;
            }
        }
        ct = next;
    }
    ct.values().sum()
}

fn part1(input: &str) -> usize {
    blinker(input, 25)
}

fn part2(input: &str) -> usize {
    blinker(input, 75)
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 11);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [55312 &e] [186996 &p]);
    check!("Part2" part2 [221683913164898 &p]);

    Ok(())
}
