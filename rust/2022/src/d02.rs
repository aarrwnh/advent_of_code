use self::HandShape::*;
use self::RoundResult::*;
use std::{fs::read_to_string, time::SystemTime};
use support::check_values;

fn parse_lines<'a>(input: &'a str) -> Vec<Vec<&'a str>> {
    return input
        .trim_end()
        .split("\n")
        .map(|x| x.split(" ").collect::<Vec<&'a str>>())
        .collect::<Vec<Vec<&'a str>>>();
}

#[derive(Debug, PartialEq)]
enum RoundResult {
    Win = 6,
    Lose = 0,
    Draw = 3,
}

impl RoundResult {
    fn value(&self) -> i8 {
        match *self {
            Win => Win as i8,
            Lose => Lose as i8,
            Draw => Draw as i8,
        }
    }
}

#[derive(Copy, Clone, Debug, PartialEq)]
enum HandShape {
    Rock = 1,
    Paper = 2,
    Scissors = 3,
}

impl HandShape {
    fn value(&self) -> i8 {
        match *self {
            Rock => Rock as i8,
            Paper => Paper as i8,
            Scissors => Scissors as i8,
        }
    }
}

trait GameOutcomes {
    fn outcomes(&self) -> Outcome;
}

struct Outcome {
    win: HandShape,
    lose: HandShape,
}

impl GameOutcomes for HandShape {
    fn outcomes(&self) -> Outcome {
        match *self {
            Rock => Outcome {
                win: Scissors,
                lose: Paper,
            },
            Paper => Outcome {
                win: Rock,
                lose: Scissors,
            },
            Scissors => Outcome {
                win: Paper,
                lose: Rock,
            },
        }
    }
}

fn one_normal_round(my_hand: HandShape, elf_hand: HandShape) -> i8 {
    let (me, elf) = (my_hand.outcomes(), elf_hand.outcomes());
    match (me.win, elf.win) {
        _ if me.win == elf_hand => Win.value(),
        _ if elf.win == my_hand => Lose.value(),
        _ => Draw.value(),
    }
}

fn one_intentional_round(expected_result: RoundResult, elf_hand: HandShape) -> i8 {
    let elf = elf_hand.outcomes();
    let my_hand = elf.lose;
    match expected_result {
        Lose => Lose.value() + elf.win.value(),
        Draw => Draw.value() + elf_hand.value(),
        Win => Win.value() + my_hand.value(),
    }
}

fn new_hand(letter: &str) -> HandShape {
    match letter {
        "X" | "A" => Rock,
        "Y" | "B" => Paper,
        "Z" | "C" => Scissors,
        _ => unreachable!(),
    }
}

fn part1(input: &str) -> u32 {
    return parse_lines(&input).iter().fold(0, |acc, x| {
        let elf_hand = new_hand(x[0]);
        let my_hand = new_hand(x[1]);
        let mut result = one_normal_round(my_hand, elf_hand);
        result += my_hand.value();
        return acc + (result as u32);
    });
}

fn part2(input: &str) -> u32 {
    return parse_lines(&input).iter().fold(0, |acc, x| {
        let elf_hand = new_hand(x[0]);
        let planned_result = match x[1] {
            "X" => Lose,
            "Y" => Draw,
            "Z" => Win,
            _ => unreachable!(),
        };
        let result = one_intentional_round(planned_result, elf_hand);
        return acc + (result as u32);
    });
}

pub fn main() {
    // [["A", "Y"], ["B", "X"], ["C", "Z"]];
    let sample = "A Y\nB X\nC Z";
    let puzzle = read_to_string("../input/2022/02/puzzle.input").unwrap();

    check_values!(15, part1, &sample);
    check_values!(11841, part1, &puzzle);

    check_values!(12, part2, &sample);
    check_values!(13022, part2, &puzzle);
}
