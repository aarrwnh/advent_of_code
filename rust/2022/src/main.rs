use aoc2022::*;
use std::{env, fmt::Error};

fn main() -> Result<(), Error> {
    let args: Vec<String> = env::args().collect();
    let day = args[1].parse::<u32>().unwrap();

    let solve = match day {
        1 => d01::main,
        2 => d02::main,
        3 => d03::main,
        4 => d04::main,
        // 5 => d05::main,
        6 => d06::main,
        _ => panic!("Unimplemented"),
    };

    match solve() {
        Err(e) => println!("{:?}", e),
        _ => (),
    }

    Ok(())
}
