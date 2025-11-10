use std::collections::HashMap;

use utils::*;

// https://en.wikipedia.org/wiki/Modular_exponentiation

fn main() {
    let input = InputReader::new("e1", 1);
    check!(part1 <-      9330868967 ; &input.load(1));
    check!(part2 <- 175478342293345 ; &input.load(2));
    check!(part3 <- 686293803275003 ; &input.load(3));
}

fn part1(input: &str) -> u64 {
    compute(input, eni)
}

fn part2(input: &str) -> u64 {
    compute(input, eni_count_5)
}

fn part3(input: &str) -> u64 {
    compute(input, eni_sum)
}

fn compute(input: &str, func: fn(u64, u64, u64) -> u64) -> u64 {
    let mut max = 0;
    for line in input.trim().split("\n") {
        let mut values = line
            .split(' ')
            .map(|x| x[2..].parse::<u64>().unwrap())
            .collect::<Vec<_>>();
        let mod_ = values.pop().unwrap();
        let result = (0..values.len() / 2)
            .map(|i| func(values[i], values[i + 3], mod_))
            .sum::<u64>();
        max = max.max(result);
    }
    max
}

fn eni(n: u64, exp: u64, mod_: u64) -> u64 {
    let mut score = 1;
    let mut s = vec![];
    for i in 0..exp {
        score = (score * n) % mod_;
        s.push(score);
    }
    convert_output(&mut s)
}

fn eni_count_5(n: u64, exp: u64, mod_: u64) -> u64 {
    let mut score = if exp > 5 {
        mod_pow(n, exp - 5, mod_)
    } else {
        1
    };
    let mut s = vec![];
    for i in 0..exp {
        score = (score * n) % mod_;
        s.push(score);
        if s.len() == 5 {
            break;
        }
    }
    convert_output(&mut s)
}

fn convert_output(s: &mut [u64]) -> u64 {
    s.reverse();
    s.iter()
        .map(ToString::to_string)
        .collect::<String>()
        .parse::<u64>()
        .unwrap()
}

fn mod_pow(mut n: u64, mut exp: u64, mod_: u64) -> u64 {
    let mut result = 1; // start % mod_;
    n %= mod_;
    while exp > 0 {
        if exp % 2 == 1 {
            result = (n * result) % mod_;
        }
        exp >>= 1;
        n = (n * n) % mod_;
    }
    result
}

fn eni_sum(n: u64, exp: u64, mod_: u64) -> u64 {
    let mut sum = 0;
    let mut score = 1;
    let mut prev = HashMap::new();
    let mut i = 0;
    while i < exp {
        score = (score * n) % mod_;
        sum += score;
        i += 1;
        if let Some((prev_i, prev_sum)) = prev.get(&score) {
            let delta_i = i - prev_i;
            let delta_sum = sum - prev_sum;
            let amount = (exp - i) / delta_i;
            sum += delta_sum * amount;
            i += delta_i * amount;
        }
        prev.insert(score, (i, sum));
    }
    sum
}

#[cfg(test)]
mod q01 {
    use super::*;

    const INPUT1: &str = "
A=4 B=4 C=6 X=3 Y=4 Z=5 M=11
A=8 B=4 C=7 X=8 Y=4 Z=6 M=12
A=2 B=8 C=6 X=2 Y=4 Z=5 M=13
A=5 B=9 C=6 X=8 Y=6 Z=8 M=14
A=5 B=9 C=7 X=6 Y=6 Z=8 M=15
A=8 B=8 C=8 X=6 Y=9 Z=6 M=16";
    const INPUT2: &str = "
A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145";

    #[test]
    fn part1_example() {
        assert_eq!(11611972920, part1(INPUT1));
    }

    #[test]
    fn part2_example1() {
        let input = "
A=4 B=4 C=6 X=3 Y=14 Z=15 M=11
A=8 B=4 C=7 X=8 Y=14 Z=16 M=12
A=2 B=8 C=6 X=2 Y=14 Z=15 M=13
A=5 B=9 C=6 X=8 Y=16 Z=18 M=14
A=5 B=9 C=7 X=6 Y=16 Z=18 M=15
A=8 B=8 C=8 X=6 Y=19 Z=16 M=16";
        assert_eq!(11051340, part2(input));
    }

    #[test]
    fn part2_example2() {
        assert_eq!(1507702060886, part2(INPUT2));
    }

    #[test]
    fn part3_example1() {
        let input = "
A=4 B=4 C=6 X=3000 Y=14000 Z=15000 M=110
A=8 B=4 C=7 X=8000 Y=14000 Z=16000 M=120
A=2 B=8 C=6 X=2000 Y=14000 Z=15000 M=130
A=5 B=9 C=6 X=8000 Y=16000 Z=18000 M=140
A=5 B=9 C=7 X=6000 Y=16000 Z=18000 M=150
A=8 B=8 C=8 X=6000 Y=19000 Z=16000 M=160";
        assert_eq!(3279640, part3(input));
    }

    #[test]
    fn asdf() {
        println!("{}", mod_pow(4, 3000, 110));
    }

    #[test]
    fn part3_example2() {
        assert_eq!(7276515438396, part3(INPUT2));
    }
}
