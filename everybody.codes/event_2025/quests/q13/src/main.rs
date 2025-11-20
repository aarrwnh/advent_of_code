use std::collections::VecDeque;

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 13);
    check!(part1 <-    381 ; &input.load(1));
    check!(part2 <-   6571 ; &input.load(2));
    check!(part3 <- 520165 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    let mut nums = vec![1];
    let mut clockwise = true;
    let mut idx = 2025;

    for num in input.trim().lines().map(|n| n.parse::<usize>().unwrap()) {
        if clockwise {
            nums.push(num);
        } else {
            nums.insert(0, num);
            idx += 1;
        }
        clockwise = !clockwise;
    }

    nums[idx % nums.len()]
}

fn part2(input: &str) -> usize {
    let mut nums = VecDeque::from([1]);
    let mut clockwise = true;
    let mut idx = 0;

    for [r1, r2] in input.trim().lines().map(|line| {
        line.split_once('-')
            .map(|x| [x.0, x.1].map(|n| n.parse::<isize>().unwrap()))
            .unwrap()
    }) {
        assert!(r1 < r2);
        if clockwise {
            nums.extend(r1..=r2);
        } else {
            let p = nums.len();
            for n in r1..=r2 {
                nums.push_front(n);
                idx += 1;
            }
        }
        clockwise = !clockwise;
    }

    nums.rotate_left(idx);

    nums[20252025 % nums.len()] as usize
}

fn part3(input: &str) -> usize {
    let mut nums = vec![(1, 1)];
    let mut clockwise = true;
    let mut idx = 0;

    for [r1, r2] in input.trim().lines().map(|line| {
        line.split_once('-')
            .map(|x| [x.0, x.1].map(|n| n.parse::<isize>().unwrap()))
            .unwrap()
    }) {
        assert!(r1 < r2);
        if clockwise {
            nums.push((r1, r2));
            idx += 1;
        } else {
            nums.insert(0, (r2, r1));
        }
        clockwise = !clockwise;
    }

    let (left, right) = nums.split_at(idx);
    let nums = [right, left].concat();
    let len = nums.iter().map(|(a, b)| (a - b).abs() + 1).sum::<isize>();
    let mut idx = 202520252025 % len;

    for (a, b) in nums {
        let c = (a - b).abs();
        if idx > c {
            idx -= c + 1;
            continue;
        }
        if a > b {
            return (a - idx) as usize;
        }
        return (a + idx) as usize;
    }

    unreachable!()
}

#[cfg(test)]
mod q13 {
    use super::*;

    #[test]
    fn part1_example() {
        let s = "
72
58
47
61
67";
        assert_eq!(67, part1(s));
    }

    #[test]
    fn part2_example() {
        let s = "
10-15
12-13
20-21
19-23
30-37";
        assert_eq!(30, part2(s));
    }
}
