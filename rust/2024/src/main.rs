use aoc2024::*;
use std::{env, error::Error, str::FromStr};

#[derive(Debug)]
enum Select {
    All,
    Day(usize),
    Last,
}

impl FromStr for Select {
    type Err = Box<dyn Error>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(match s.parse::<usize>().ok().unwrap() {
            0 => Self::All,
            d @ 1..25 => Self::Day(d),
            _ => Self::Last,
        })
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let day = args
        .get(1)
        .map_or_else(|| Select::Last, |s| Select::from_str(s).unwrap());
    let lst = [
        d01::main,
        d02::main,
        d03::main,
        d04::main,
        d05::main,
        d06::main,
        d07::main,
        d08::main,
        // d09::main,
        // d10::main,
        d11::main,
        // d12::main,
        // d13::main,
        // d14::main,
        // d15::main,
        // d16::main,
        // d17::main,
        // d18::main,
        // d19::main,
        // d20::main,
        // d21::main,
        // d22::main,
        // d23::main,
        // d24::main,
        // d25::main,
    ];

    match day {
        Select::All => {
            for (i, module) in lst.iter().enumerate() {
                println!(" == Day {} ==", i + 1);
                module()?;
            }
        }
        Select::Day(d) => {
            println!(" == Day {} ==", d);
            lst[d]()?
        },
        Select::Last => lst.last().unwrap()()?,
    };

    Ok(())
}
