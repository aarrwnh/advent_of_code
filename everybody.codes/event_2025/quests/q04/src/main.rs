use utils::*;

fn main() {
    let input = InputReader::new("e2025", 4);
    check!(part1 <-         10602 ; &input.load(1));
    check!(part2 <- 1618852459017 ; &input.load(2));
    check!(part3 <-  927893273384 ; &input.load(3));
}

fn parse(s: &str) -> u64 {
    s.parse::<u64>().unwrap()
}

fn div(input: &str) -> f64 {
    let nums: Vec<u64> = input.trim().lines().map(|x| parse(x)).collect();
    nums[0] as f64 / nums[nums.len() - 1] as f64
}

fn part1(input: &str) -> u64 {
    (2025.0 * div(input)).floor() as u64
}

fn part2(input: &str) -> u64 {
    (10_000_000_000_000.0 / div(input)).ceil() as u64
}

fn part3(input: &str) -> u64 {
    let mut t = 1.0;
    for p in input.trim().split('|').map(|p| p.split_once('\n')) {
        t *= p.map(|(a, b)| parse(a) as f64 / parse(b) as f64).unwrap();
    }
    (t * 100.0) as u64
}

#[cfg(test)]
mod q04 {
    use super::*;

    #[test]
    fn part3_example() {
        let input = "
5
7|21
18|36
27|27
10|50
10|50
11";
        assert_eq!(6818, part3(input));
    }
}
