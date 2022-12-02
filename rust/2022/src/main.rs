use aoc2022::*;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let day = args[1].parse::<u32>().unwrap();
    let solve = match day {
        1 => d01::main,
        2 => d02::main,
        _ => panic!("Unimplemented"),
    };

    solve();
}
