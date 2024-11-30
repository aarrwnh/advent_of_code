use self::HandShape::*;
use self::Letter::*;
use self::RoundResult::*;
use std::error::Error;
use std::fs::read_to_string;
use std::str::FromStr;
use support::*;

#[derive(Debug, Copy, Clone, PartialEq, PartialOrd, Eq, Ord)]
enum Letter {
    A,
    B,
    C,
    X,
    Y,
    Z,
}

impl TryFrom<&str> for Letter {
    type Error = String;

    fn try_from(ch: &str) -> Result<Self, Self::Error> {
        Ok(match ch {
            "A" => A,
            "B" => B,
            "C" => C,
            "X" => X,
            "Y" => Y,
            "Z" => Z,
            _ => unreachable!(),
        })
    }
}

#[derive(Debug)]
struct Input(Vec<(Letter, Letter)>);

impl FromStr for Input {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self(
            s.trim_end()
                .split('\n')
                .map(|x| {
                    let a = x
                        .split(' ')
                        .map(|c| Letter::try_from(c).ok().unwrap())
                        .collect::<Vec<_>>();
                    (a[0], a[1])
                })
                .collect::<_>(),
        ))
    }
}

// fn parse_lines<'a>(input: &'a str) -> Vec<Vec<&'a str>> {
//     input
//         .trim_end()
//         .split('\n')
//         .map(|x| x.split(' ').collect::<Vec<&'a str>>())
//         .collect::<Vec<Vec<&'a str>>>()
// }

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

fn new_hand(letter: Letter) -> HandShape {
    match letter {
        X | A => Rock,
        Y | B => Paper,
        Z | C => Scissors,
    }
}

fn part1(input: &Input) -> u32 {
    input.0.iter().fold(0, |acc, x| {
        let elf_hand = new_hand(x.0);
        let my_hand = new_hand(x.1);
        let mut result = one_normal_round(my_hand, elf_hand);
        result += my_hand.value();
        acc + (result as u32)
    })
}

fn part2(input: &Input) -> u32 {
    input.0.iter().fold(0, |acc, x| {
        let elf_hand = new_hand(x.0);
        let planned_result = match x.1 {
            X => Lose,
            Y => Draw,
            Z => Win,
            _ => unreachable!(),
        };
        let result = one_intentional_round(planned_result, elf_hand);
        acc + (result as u32)
    })
}

pub fn main() -> Result<(), Box<dyn Error>> {
    // [["A", "Y"], ["B", "X"], ["C", "Z"]];
    let example = "A Y\nB X\nC Z";
    let i = InputReader::new(2022, 2);
    let p = Input::from_str(&i.as_raw("puzzle")).unwrap();
    let e = Input::from_str(example).unwrap();

    check!("Part1" part1 [15 &e] [11841 &p]);
    check!("Part2" part2 [12 &e] [13022 &p]);

    Ok(())
}
