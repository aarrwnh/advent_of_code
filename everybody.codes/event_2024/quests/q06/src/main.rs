use std::collections::{HashMap, VecDeque};

use utils::*;

fn main() {
    let input = InputReader::new("e2024", 6);
    check!(part1 <- "RRRDSZZGKHPL@" ; &input.load(1));
    check!(part2 <-   "RPDHPMFWTW@" ; &input.load(2));
    check!(part3 <- "RDSCNBGPCFPN@" ; &input.load(3));
}

const START: &str = "RR";
const END: &str = "@";

fn part1(input: &'_ str) -> String {
    Trees::from(input).find_whole()
}

fn part2(input: &'_ str) -> String {
    Trees::from(input).find_first_letter()
}

fn part3(input: &'_ str) -> String {
    Trees::from(input).find_first_letter()
}

type Branches<'a> = HashMap<&'a str, Vec<&'a str>>;

struct Trees<'input> {
    branches: Branches<'input>,
}

fn traverse<E>(branches: &Branches<'_>, extract: E) -> Option<String>
where
    E: FnOnce(&[&'_ str]) -> String,
{
    let mut qu = VecDeque::from([(START, vec![START])]);
    let mut paths: HashMap<usize, Vec<Vec<&'_ str>>> = HashMap::new();
    while let Some((current, path)) = qu.pop_front() {
        if current == END {
            paths.entry(path.len()).or_default().push(path);
        } else if let Some(it) = branches.get(current) {
            for n in it {
                let mut path = path.clone();
                path.push(n);
                qu.push_back((n, path));
            }
        }
    }
    for p in paths.values() {
        if p.len() == 1 {
            return p.get(0).map(|x| extract(x));
        }
    }
    None
}

fn is_invalid(s: &str) -> bool {
    s.starts_with("ANT") || s.starts_with("BUG")
}

impl<'input> Trees<'input> {
    fn from(input: &'input str) -> Self {
        Self {
            branches: input
                .trim()
                .lines()
                .filter_map(|line| {
                    if is_invalid(&line[..3]) {
                        None
                    } else if let Some((left, right)) = line.split_once(':') {
                        let right = right
                            .split(',')
                            .filter(|s| !is_invalid(s))
                            .collect::<Vec<_>>();
                        Some((left, right))
                    } else {
                        panic!()
                    }
                })
                .collect(),
        }
    }

    fn find_whole(&self) -> String {
        traverse(&self.branches, |path| path.iter().map(|x| *x).collect()).unwrap()
    }

    fn find_first_letter(&self) -> String {
        traverse(&self.branches, |path| {
            path.iter()
                .filter_map(|branch| branch.chars().next())
                .collect()
        })
        .unwrap()
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "
RR:A,B,C
A:D,E
B:F,@
C:G,H
D:@
E:@
F:@
G:@
H:@";
        assert_eq!("RRB@", Trees::from(input).find_whole());
    }
}
