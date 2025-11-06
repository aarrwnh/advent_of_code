use std::str::FromStr;

use Inst::*;
use utils::*;

fn main() {
    let input = InputReader::new("e2025", 1);
    check!(part1 <-  "Tharindor" ; &input.load(1));
    check!(part2 <-  "Irynnixis" ; &input.load(2));
    check!(part3 <- "Cynderbryn" ; &input.load(3));
}

fn part1(input: &str) -> String {
    Shell::from(input).part1()
}

fn part2(input: &str) -> String {
    Shell::from(input).part2()
}

fn part3(input: &str) -> String {
    Shell::from(input).part3()
}

struct Shell<'a> {
    names: Vec<&'a str>,
    instructions: Box<dyn Iterator<Item = Inst> + 'a>,
}

impl<'a> Shell<'a> {
    fn from(s: &'a str) -> Self {
        let Some((names, instructions)) = s.trim().split_once("\n\n") else {
            panic!()
        };
        Self {
            names: names.split(',').collect::<Vec<_>>(),
            instructions: Box::new(instructions.split(',').map(|x| x.parse().unwrap())),
        }
    }

    fn part1(self) -> String {
        let mut idx = 0;
        let total = self.names.len() as isize;
        for inst in self.instructions {
            idx += inst.offset();
            if idx < 0 {
                idx = 0;
            } else if idx >= total {
                idx = total - 1;
            };
        }
        self.names[idx as usize].to_string()
    }

    fn part2(self) -> String {
        let idx = &self.instructions.fold(0, |acc, inst| acc + inst.offset());
        self.names[*idx as usize % self.names.len()].to_string()
    }

    fn part3(self) -> String {
        let Self {
            mut names,
            instructions: inst,
        } = self;
        let total = names.len() as isize;
        for inst in inst {
            let idx = (match inst {
                Left(n) => n.rem_euclid(total),
                Right(n) => n,
            } % total) as usize;
            [names[0], names[idx]] = [names[idx], names[0]];
        }
        names[0].to_string()
    }
}

enum Inst {
    Left(isize),
    Right(isize),
}

impl Inst {
    const fn offset(self) -> isize {
        match self {
            Left(n) | Right(n) => n,
        }
    }
}

impl FromStr for Inst {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut chars = s.chars();
        let dir = chars.next().unwrap();
        let offset = chars
            .collect::<String>()
            .parse::<isize>()
            .unwrap();
        match dir {
            'L' => Ok(Left(-offset)),
            'R' => Ok(Right(offset)),
            _ => panic!("invalid char: {dir}"),
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;
    const EXAMPLE: &str = "
Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L1";

    #[test]
    fn part1_example() {
        assert_eq!("Fyrryn", part1(EXAMPLE));
    }

    #[test]
    fn part2_example() {
        assert_eq!("Elarzris", part2(EXAMPLE));
    }

    #[test]
    fn part3_example() {
        let input = "
Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L3";
        assert_eq!("Drakzyph", part3(input));
    }
}
