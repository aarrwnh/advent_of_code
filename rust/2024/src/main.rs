use aoc2024::*;
use std::{env, error::Error};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let day = args[1].parse()?;
    let lst = [
        d01::main,
        d02::main,
        d03::main,
        d04::main,
        d05::main,
        d06::main,
        // d07::main,
        // d08::main,
        // d09::main,
        // d10::main,
        // d11::main,
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
