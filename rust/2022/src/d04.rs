use std::{error::Error, fs::read_to_string, time::SystemTime};
use support::check_values;

fn split_pairs(pair: &str) -> (u16, u16, u16, u16) {
    // let aa: Vec<u16> = pair
    //     .split(&[',', '-'][..])
    //     .map(|s| s.parse::<u16>().unwrap())
    //     .collect();
    // let [a, b, c, d] = &aa[..] else { todo!() };
    // (*a, *b, *c, *d)

    let (p1, p2) = pair.split_once(",").expect("");
    let (a, b) = p1.split_once("-").expect("");
    let (c, d) = p2.split_once("-").expect("");
    (
        a.parse::<u16>().unwrap(),
        b.parse::<u16>().unwrap(),
        c.parse::<u16>().unwrap(),
        d.parse::<u16>().unwrap(),
    )
}

fn part1(pairs: &[&str]) -> u32 {
    let mut total = 0;
    for &pair in pairs {
        let (a, b, c, d) = split_pairs(&pair);
        if a >= c && b <= d || c >= a && d <= b {
            total += 1;
        };
    }
    return total;
}

fn part2(pairs: &[&str]) -> u32 {
    let mut total = 0;
    for &pair in pairs {
        let (a, b, c, d) = split_pairs(&pair);
        let r = c..=d;
        for i in a..=b {
            if r.contains(&i) {
                total += 1;
                break;
            }
        }
    }
    return total;
}

pub fn main() -> Result<(), Box<dyn Error>> {
    let sample: String = read_to_string("../input/2022/04/sample.input")?.parse()?;
    let sample = sample.lines().collect::<Vec<&str>>();
    let puzzle: String = read_to_string("../input/2022/04/puzzle.input")?.parse()?;
    let puzzle = puzzle.lines().collect::<Vec<&str>>();

    check_values!(2, part1, &sample);
    check_values!(569, part1, &puzzle);

    check_values!(4, part2, &sample);
    check_values!(936, part2, &puzzle);

    Ok(())
}
