use std::cmp::Ordering;
use std::str::FromStr;

use support::{check, InputReader};

fn read_chars(input: &str, part2: bool) -> u64 {
    let mut total = 0;
    let mut cursor = 0;
    let mut enabled = true;
    loop {
        if cursor + 4 > input.len() {
            break;
        }
        cursor += match &input[cursor..cursor + 4] {
            "do()" => {
                if part2 {
                    enabled = true;
                }
                4
            }
            "don'" => {
                if part2 {
                    enabled = false;
                }
                7
            }
            "mul(" => {
                let mut end = 4;
                if enabled {
                    let chunk = &input[cursor + end..];
                    if let Some(i) = chunk.find(")") {
                        if let Some((l, r)) = chunk[..i].split_once(",") {
                            let v = [l, r].map(|x| x.parse::<u64>().ok());
                            if let [Some(l), Some(r)] = v {
                                total += l * r;
                                end = i + 1;
                            }
                        }
                    }
                }
                end
            }
            _ => 1,
        }
    }
    total
}

fn part1(input: &str) -> u64 {
    read_chars(input, false)
}

fn part2(input: &str) -> u64 {
    read_chars(input, true)
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 3);
    let e = &i.as_raw("example");
    let p = &i.as_raw("puzzle");

    check!("Part1" part1 [161 &e] [155955228 &p]);

    let e = "xmul(2,4)&mul[3,7]!^don't()do()don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
    check!("Part2" part2 [48 &e] [100189366 &p]);

    Ok(())
}
