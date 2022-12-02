use self::HandResult::*;
use self::HandShape::*;
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
enum HandResult {
    Win,
    Lose,
    Draw,
}

#[derive(Copy, Clone, Debug, PartialEq)]
enum HandShape {
    Rock = 1,
    Paper = 2,
    Scissors = 3,
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

fn one_round(my_hand: HandShape, elf_hand: HandShape) -> i8 {
    let (me, elf) = (my_hand.outcomes(), elf_hand.outcomes());
    match (me.win, elf.win) {
        _ if me.win == elf_hand => 6, // win,
        _ if elf.win == my_hand => 0, // lose,
        _ => 3,                       // draw,
    }
}

fn one_round_expect(expected_result: HandResult, elf_hand: HandShape) -> i8 {
    let elf = elf_hand.outcomes();
    let my_hand = elf.lose;
    match expected_result {
        Lose => 0 + (elf.win as i8),
        Draw => 3 + (elf_hand as i8),
        Win => 6 + (elf.lose as i8),
    }
}

fn part1(input: &str) -> u32 {
    return parse_lines(&input).iter().fold(0, |acc, x| {
        let elf_hand = match x[0] {
            "A" => Rock,
            "B" => Paper,
            "C" => Scissors,
            _ => unreachable!(),
        };
        let my_hand = match x[1] {
            "X" => Rock,
            "Y" => Paper,
            "Z" => Scissors,
            _ => unreachable!(),
        };
        let mut result = one_round(my_hand, elf_hand);
        result += my_hand as i8;
        return acc + (result as u32);
    });
}

fn part2(input: &str) -> u32 {
    return parse_lines(&input).iter().fold(0, |acc, x| {
        let elf_hand = match x[0] {
            "A" => Rock,
            "B" => Paper,
            "C" => Scissors,
            _ => unreachable!(),
        };
        let expected_result = match x[1] {
            "X" => Lose,
            "Y" => Draw,
            "Z" => Win,
            _ => unreachable!(),
        };
        let result = one_round_expect(expected_result, elf_hand);
        return acc + (result as u32);
    });
}

pub fn main() {
    // [["A", "Y"], ["B", "X"], ["C", "Z"]];
    let sample = "A Y\nB X\nC Z".to_string();
    let puzzle = read_to_string("../input/2022/02/puzzle.input").unwrap();

    check_values!(15, part1, &sample);
    check_values!(11841, part1, &puzzle);

    check_values!(12, part2, &sample);
    check_values!(13022, part2, &puzzle);
}
