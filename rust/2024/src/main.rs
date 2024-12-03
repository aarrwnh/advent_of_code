use aoc2024::*;
use std::{env, error::Error};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let day = args[1].parse()?;
    let lst = [d01::main, d02::main, d03::main];

    match day {
        0 => {
            for (i, module) in lst.iter().enumerate() {
                println!(" == Day {} ==", i + 1);
                module()?;
            }
        }
        d if (1..=lst.len()).contains(&d) => lst.get(day - 1).unwrap()()?,
        _ => panic!("Unimplemented"),
    };

    Ok(())
}
