use utils::*;

fn main() {
    let input = InputReader::new("e2024", 1);
    check!(part1 <-  1377 ; &input.load(1));
    check!(part2 <-  5458 ; &input.load(2));
    check!(part3 <- 27556 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    Mons::chunks(1, &input)
}

fn part2(input: &str) -> usize {
    Mons::chunks(2, &input)
}

fn part3(input: &str) -> usize {
    Mons::chunks(3, &input)
}

#[derive(PartialEq, Debug)]
enum Mons {
    A,
    B,
    C,
    D,
    X,
}

impl From<char> for Mons {
    fn from(value: char) -> Self {
        match value {
            'A' => Self::A,
            'B' => Self::B,
            'C' => Self::C,
            'D' => Self::D,
            'x' => Self::X,
            _ => panic!("{value} is not supported"),
        }
    }
}

impl Mons {
    fn to_value(&self) -> usize {
        match self {
            Mons::B => 1,
            Mons::C => 3,
            Mons::D => 5,
            _ => 0,
        }
    }

    fn is_empty(&self) -> bool {
        *self == Self::X
    }

    fn chunks(chunks: usize, input: &str) -> usize {
        let it = input.chars().map(Into::<Mons>::into);
        if chunks == 1 {
            it.map(|m| m.to_value()).sum()
        } else if input.len() % chunks == 0 {
            it.collect::<Vec<_>>()
                .chunks(chunks)
                .fold(0, |mut acc, monsters| {
                    let mut count = 0;
                    for m in monsters
                        .iter()
                        .filter(|m| !m.is_empty())
                        .map(Mons::to_value)
                    {
                        acc += m;
                        count += 1;
                    }
                    acc += match count {
                        2 => 2,
                        3 => 6,
                        _ => 0,
                    };
                    acc
                })
        } else {
            0
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part3() {
        assert_eq!(30, Mons::chunks(3, "xBxAAABCDxCC"));
    }
}
