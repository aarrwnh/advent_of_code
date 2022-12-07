use std::{error::Error, fs::read_to_string, time::SystemTime};
use support::check_values;

fn read_signal(input: &str, start: usize) -> u32 {
    let mut q: Vec<u8> = Vec::with_capacity(start);
    for (i, &c) in input.as_bytes().iter().enumerate() {
        q.push(c);
        if q.len() > start {
            q.remove(0);
            if q.iter()
                .all(|&c| q.iter().filter(|&&d| c == d).count() == 1)
            {
                return (i as u32) + 1;
            }
        }
    }
    unreachable!("1")
}

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
fn read_signal_bitwise(input: &str, size: usize) -> u32 {
    let o = input.as_bytes().windows(size).position(move |set| {
        let mut data: u32 = 0;
        for &c in set {
            let prev = data;
            data |= 1 << (c - b'a');
            if prev == data {
                return false;
            }
        }
        return true;
    });
    (o.unwrap() + size) as u32
}

/// by @_B_3_N_N_Y_
fn read_signal_bitwise2(input: &str, size: usize) -> u32 {
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
    read_signal(input, 4)
}

fn part2(input: &str) -> u32 {
    read_signal(input, 14)
}

pub fn main() -> Result<(), Box<dyn Error>> {
    let sample: String = read_to_string("../input/2022/06/sample.input")?.parse()?;
    let puzzle: String = read_to_string("../input/2022/06/puzzle.input")?.parse()?;

    check_values!(7, part1, &sample);
    check_values!(1093, part1, &puzzle);

    check_values!(19, part2, "mjqjpqmgbljsphdztnvjfqwrcgsmlb");
    check_values!(3534, part2, &puzzle);

    Ok(())
}
