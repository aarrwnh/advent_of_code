use std::{cmp::Ordering, str::FromStr};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 5);
    check!(part1 <-  "4735746267" ; &input.load(1));
    check!(part2 <- 8636531677060 ; &input.load(2));
    check!(part3 <-      31624831 ; &input.load(3));
}

fn part1(input: &str) -> String {
    Fishbone::from_str(input.trim())
        .unwrap()
        .quality
        .to_string()
}

fn part2(input: &str) -> u64 {
    let mut res = input
        .trim()
        .lines()
        .map(|line| Fishbone::from_str(line).unwrap().quality)
        .collect::<Vec<_>>();
    res.sort_unstable();
    res[res.len() - 1] - res[0]
}

fn part3(input: &str) -> u64 {
    let mut res = Vec::new();
    for line in input.trim().lines() {
        res.push(Fishbone::from_str(line).unwrap());
    }
    res.sort_by(compare);
    res.iter()
        .rev()
        .enumerate()
        .map(|(i, x)| (i as u64 + 1) * x.id)
        .sum()
}

struct Fishbone {
    id: u64,
    levels: Vec<u64>,
    quality: u64,
}

impl FromStr for Fishbone {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (id, nums) = s.split_once(':').unwrap();

        let mut levels: Vec<Level<_>> = vec![];
        for num in nums.split(',').map(|x| x.parse().unwrap()) {
            let mut insert_blank = true;
            for cur in &mut levels {
                if cur.try_insert(num) {
                    insert_blank = false;
                    break;
                }
            }
            if insert_blank {
                levels.push(Level::new(num));
            }
        }

        let mut quality = String::new();
        let levels = levels
            .iter()
            .map_while(|n| {
                if n.middle.is_none() {
                    None
                } else {
                    quality.push_str(&n.middle());
                    Some(n.as_num())
                }
            })
            .collect();
        Ok(Self {
            id: id.parse().unwrap(),
            quality: quality.parse().unwrap(),
            levels,
        })
    }
}

#[derive(Default)]
struct Level<T> {
    middle: Option<T>,
    left: Option<T>,
    right: Option<T>,
}

impl<T> Level<T>
where
    T: PartialOrd + ToString + Copy + FromStr,
    T: std::fmt::Debug,
    T::Err: std::fmt::Debug,
{
    fn middle(&self) -> String {
        self.middle.unwrap().to_string()
    }

    fn try_insert(&mut self, num: T) -> bool {
        let root = self.middle.unwrap();
        if num < root && self.left.is_none() {
            self.left.replace(num);
            return true;
        } else if num > root && self.right.is_none() {
            self.right.replace(num);
            return true;
        }
        false
    }

    // join numbers into level quality
    fn as_num(&self) -> T {
        [self.left, self.middle, self.right]
            .iter()
            .filter_map(|x| x.as_ref().map(ToString::to_string))
            .collect::<String>()
            .parse()
            .unwrap()
    }

    const fn new(num: T) -> Self {
        Self {
            middle: Some(num),
            left: None,
            right: None,
        }
    }
}

fn compare(a: &Fishbone, b: &Fishbone) -> Ordering {
    match a.quality.cmp(&b.quality) {
        Ordering::Equal => {}
        c => return c,
    }

    for (a1, b1) in a.levels.iter().zip(b.levels.iter()) {
        match a1.cmp(b1) {
            Ordering::Equal => {}
            c => return c,
        }
    }

    a.id.cmp(&b.id)
}

#[cfg(test)]
mod q05 {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "58:5,3,7,8,9,10,4,5,7,8,8";
        assert_eq!("581078", part1(input));
    }

    #[test]
    fn part2_example() {
        let input = "
1:2,4,1,1,8,2,7,9,8,6
2:7,9,9,3,8,3,8,8,6,8
3:4,7,6,9,1,8,3,7,2,2
4:6,4,2,1,7,4,5,5,5,8
5:2,9,3,8,3,9,5,2,1,4
6:2,4,9,6,7,4,1,7,6,8
7:2,3,7,6,2,2,4,1,4,2
8:5,1,5,6,8,3,1,8,3,9
9:5,7,7,3,7,2,3,8,6,7
10:4,1,9,3,8,5,4,3,5,5";
        assert_eq!(77053, part2(input));
    }

    #[test]
    fn part3_example() {
        let input = "
1:7,1,9,1,6,9,8,3,7,2
2:6,1,9,2,9,8,8,4,3,1
3:7,1,9,1,6,9,8,3,8,3
4:6,1,9,2,8,8,8,4,3,1
5:7,1,9,1,6,9,8,3,7,3
6:6,1,9,2,8,8,8,4,3,5
7:3,7,2,2,7,4,4,6,3,1
8:3,7,2,2,7,4,4,6,3,7
9:3,7,2,2,7,4,1,6,3,7";
        assert_eq!(260, part3(input));
    }
}
