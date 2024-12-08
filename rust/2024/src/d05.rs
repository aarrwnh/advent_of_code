use std::{
    collections::{HashMap, VecDeque},
    ops::Range,
    str::FromStr,
};
use support::{check, InputReader};

type Rules = HashMap<u8, Vec<u8>>;

#[derive(Debug)]
struct Manual {
    rules: Rules,
    list: Vec<Vec<u8>>,
}

fn num(n: &str) -> u8 {
    u8::from_str(n).unwrap()
}

impl FromStr for Manual {
    type Err = Box<dyn std::error::Error>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(s.split_once("\n\n")
            .map(|(rules, ordering)| {
                let mut map: Rules = HashMap::new();
                rules.lines().for_each(|line| {
                    let (a, b) = line.split_once("|").unwrap();
                    map.entry(num(a)).or_default().push(num(b));
                });
                Self {
                    rules: map,
                    list: ordering
                        .lines()
                        .map(|line| line.split(",").map(num).collect::<Vec<_>>())
                        .collect::<Vec<_>>(),
                }
            })
            .unwrap())
    }
}

impl Manual {
    fn check_sorted(&self, i: usize) -> Option<u64> {
        let list = &self.list[i];
        for (i, a) in list.iter().enumerate() {
            for b in &list[i + 1..] {
                if !self.rules.get(a)?.contains(b) {
                    return None;
                }
            }
        }
        Some(list[list.len() / 2].into())
    }

    fn range(&self) -> Range<usize> {
        (0..self.list.len())
    }
}

fn part1(input: &Manual) -> u64 {
    input.range().filter_map(|i| input.check_sorted(i)).sum()
}

fn part2(input: &Manual) -> u64 {
    let Manual { rules, list } = &input;

    let sort = |numbers: &[u8]| {
        let mut indicies: HashMap<u8, u8> = HashMap::new();
        for (i, a) in numbers.iter().enumerate() {
            for b in &numbers[i + 1..] {
                if let Some(v) = rules.get(b) {
                    if v.contains(a) {
                        *indicies.entry(*a).or_default() += 1;
                    }
                }
                if let Some(v) = rules.get(a) {
                    if v.contains(b) {
                        *indicies.entry(*b).or_default() += 1;
                    }
                }
            }
        }

        let mut todo = VecDeque::new();
        let mut new_stack = Vec::new();

        for a in numbers {
            if !indicies.contains_key(a) {
                todo.push_back(*a);
                new_stack.push(*a);
            }
        }

        while let Some(a) = todo.pop_front() {
            let Some(v) = rules.get(&a) else { continue };
            for b in v {
                let Some(val) = indicies.get_mut(b) else {
                    continue;
                };
                *val -= 1;
                if *val == 0 {
                    todo.push_back(*b);
                    new_stack.push(*b);
                }
            }
        }

        new_stack
    };

    let run = |numbers: &[u8], i: usize, a: &u8| {
        for b in &numbers[i + 1..] {
            let Some(v) = rules.get(b) else { continue };
            if v.contains(a) {
                let n2 = sort(numbers);
                return Some(n2[n2.len() / 2] as u64);
            }
        }
        None
    };

    input
        .range()
        .filter_map(|i| {
            let numbers = &list[i];
            for (i, a) in numbers.iter().enumerate() {
                if let Some(v) = run(numbers, i, a) {
                    return Some(v);
                }
            }
            None
        })
        .sum()
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 5);
    let e = Manual::from_str(&i.as_raw("example"))?;
    let p = Manual::from_str(&i.as_raw("puzzle"))?;

    check!("Part1" part1 [143 &e] [5166 &p]);
    check!("Part2" part2 [123 &e] [4679 &p]);

    Ok(())
}
