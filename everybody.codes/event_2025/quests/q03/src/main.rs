use std::collections::{HashMap, HashSet};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 3);
    check!(part1 <- 2701 ; &input.load(1));
    check!(part2 <-  307 ; &input.load(2));
    check!(part3 <- 4404 ; &input.load(3));
}

fn part1(input: &str) -> u32 {
    parse::<HashSet<_>, _>(input).iter().sum()
}

fn part2(input: &str) -> u32 {
    let crates: HashSet<_> = parse(input);
    let mut crates = crates.iter().collect::<Vec<_>>();
    crates.sort();
    crates.drain(..20).sum()

    // let size = crates.len();
    // let mut optimal = u32::MAX;
    // let mut temp = vec![];
    // for i in 0..size {
    //     let mut j = i + 1;
    //     let cur = crates[i];
    //     temp.push(cur);
    //     while j < size {
    //         if crates[j] < cur {
    //             temp.push(crates[j]);
    //         }
    //         j += 1;
    //         if temp.len() == 20 {
    //             optimal = optimal.min(temp.drain(..).sum::<u32>());
    //             break;
    //         }
    //     }
    //     temp.clear();
    // }
    // optimal
}

fn part3(input: &str) -> u32 {
    let mut crates: HashMap<u8, _> = HashMap::new();
    for c in parse::<Vec<_>, u8>(input) {
        crates.entry(c).and_modify(|v| *v += 1).or_insert(1);
    }
    *crates.iter().map(|x| x.1).max().unwrap()

    // crates.sort();
    // let size = crates.len();
    // for i in 3..(size / 2) {
    //     let mut sets = vec![0; i];
    //     let mut j = 0;
    //     'a: loop {
    //         for set in &mut sets {
    //             let current = crates[j];
    //             if *set < current {
    //                 *set = current;
    //             } else {
    //                 break 'a;
    //             }
    //             j += 1;
    //             if j == size {
    //                 return i;
    //             }
    //         }
    //     }
    // }
    // unreachable!()
}

fn parse<T, F>(input: &str) -> T
where
    T: FromIterator<F>,
    F: std::str::FromStr,
    <F as std::str::FromStr>::Err: std::fmt::Debug,
{
    input
        .split(',')
        .map(|x| x.parse::<F>().unwrap())
        .collect::<T>()
}

#[cfg(test)]
mod q03 {
    use super::*;
    const INPUT1: &str = "10,5,1,10,3,8,5,2,2";
    const INPUT2: &str = "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77";

    #[test]
    fn part1_example() {
        assert_eq!(29, part1(INPUT1));
    }

    #[test]
    fn part2_example() {
        assert_eq!(781, part2(INPUT2));
    }

    #[test]
    fn part3_example() {
        assert_eq!(3, part3(INPUT2));
    }
}
