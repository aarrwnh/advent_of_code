use std::{error::Error, fs::read_to_string, time::SystemTime};

use support::{InputReader, check};

// fn read_signal(input: &str, start: usize) -> u32 {
//     let mut q: Vec<u8> = Vec::with_capacity(start);
//     for (i, &c) in input.as_bytes().iter().enumerate() {
//         q.push(c);
//         if q.len() > start {
//             q.remove(0);
//             if q.iter()
//                 .all(|&c| q.iter().filter(|&&d| c == d).count() == 1)
//             {
//                 return (i as u32) + 1;
//             }
//         }
//     }
//     unreachable!("1")
// }

// fn read_signal_slow_hashset(input: &str, start: usize) -> u32 {
//     let result = input
//         .as_bytes()
//         .windows(start)
//         .enumerate()
//         .find(|(_, w)| {
//             let mut set = HashSet::new();
//             for b in w.iter() {
//                 if !set.insert(*b) {
//                     return false;
//                 }
//             }
//             return true;
//         })
//         .unwrap();
//     return (result.0 + start) as u32;
// }

// by ThePrimeagen
// fn read_signal_bitwise(input: &str, size: usize) -> u32 {
//     (input.as_bytes().windows(size).position(move |set| {
//         let mut data: u32 = 0;
//         for &c in set {
//             let prev = data;
//             data |= 1 << (c - b'a');
//             if prev == data {
//                 return false;
//             }
//         }
//         true
//     }).unwrap() + size) as u32
// }

fn read_signal_bitwise(input: &str, size: usize) -> u32 {
    let i = input.as_bytes();

    let mut filter = 0u32;

    i.iter()
        .take(size - 1)
        .for_each(|c| filter ^= 1 << (c - b'a'));

    i.windows(size)
        .position(|w| {
            let first = w[0];
            let last = w[w.len() - 1];

            filter ^= 1 << (last - b'a');
            let res = filter.count_ones() == size as _;
            filter ^= 1 << (first - b'a');

            res
        })
        .map(|x| x + size)
        .unwrap() as u32
}

fn part1(input: &str) -> u32 {
    read_signal_bitwise(input, 4)
}

fn part2(input: &str) -> u32 {
    read_signal_bitwise(input, 14)
}

pub fn main() -> Result<(), Box<dyn Error>> {
    let i = InputReader::new(2022, 6);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [7 &e] [1093 &p]);
    check!("Part2" part2 [19 &"mjqjpqmgbljsphdztnvjfqwrcgsmlb"] [3534 &p]);

    Ok(())
}
