use utils::*;

fn main() {
    let input = InputReader::new("e2025", 11);
    check!(part1 <-             269 ; &input.load(1));
    check!(part2 <-         3306554 ; &input.load(2));
    check!(part3 <- 120440294241571 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    let rounds = 10;
    let mut nums = parse(input);
    let mut phase = 1;
    for _ in 0..=rounds {
        let mut flag = true;
        for i in 0..nums.len() - 1 {
            if phase == 1 {
                if nums[i] > nums[i + 1] {
                    flag = false;
                    nums[i] -= 1;
                    nums[i + 1] += 1;
                }
            } else if phase == 2 {
                if nums[i] < nums[i + 1] {
                    nums[i] += 1;
                    nums[i + 1] -= 1;
                }
            }
        }
        if flag {
            phase = 2;
        }
    }
    nums.iter()
        .zip(1usize..)
        .map(|(col, idx)| col * idx)
        .sum::<usize>()
}

fn part2(input: &str) -> usize {
    let mut nums = parse(input);
    let mut round = 0;
    loop {
        let mut flag = true;
        for i in 0..nums.len() - 1 {
            if nums[i] > nums[i + 1] {
                flag = false;
                nums[i] -= 1;
                nums[i + 1] += 1;
            }
        }
        if flag {
            return round + short(&nums);
        }
        // if nums.iter().all(|x| *x == nums[0]) {
        //     break;
        // }
        round += 1;
    }
}

fn part3(input: &str) -> usize {
    // assert!(a>b)
    short(&parse(input))
}

fn short(nums: &[usize]) -> usize {
    let avg = nums.iter().sum::<usize>() / nums.len();
    nums.iter().filter(|x| **x > avg).map(|x| *x - avg).sum()
}

fn parse(input: &str) -> Vec<usize> {
    input
        .trim()
        .lines()
        .map(|x| x.parse::<usize>().unwrap())
        .collect::<Vec<_>>()
}

#[cfg(test)]
mod q11 {
    use super::*;

    #[test]
    fn part1_example() {
        let s = "9\n1\n1\n4\n9\n6";
        assert_eq!(109, part1(s));
    }

    #[test]
    fn part2_example() {
        let s = "9\n1\n1\n4\n9\n6";
        assert_eq!(11, part2(s));
    }

    #[test]
    fn part2_example2() {
        let s = "805\n706\n179\n48\n158\n150\n232\n885\n598\n524\n423";
        assert_eq!(1579, part2(s));
    }
}
