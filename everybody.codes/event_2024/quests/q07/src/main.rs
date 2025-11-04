use std::{collections::HashMap, str::FromStr};

use utils::{InputReader, Permutations, check};

fn main() {
    let input = InputReader::new("e2024", 7);
    check!(part1 <- "FGECABDHK" ; &input.load(1), 10);
    check!(part2 <- "JGHKFCDIB" ; &input.load(2));
    check!(part3 <-        3868 ; &input.load(3));
}

fn part1(input: &str, total_segments: usize) -> String {
    input
        .trim()
        .lines()
        .map(Plan::from)
        .map(|plan| (plan.id, plan.run(total_segments)))
        .collect::<Vec<_>>()
        .to_sorted()
}

fn part2(input: &str) -> String {
    Track::parse(TRACK_2) //
        .run(input, 10, None)
        .to_sorted()
}

fn part3(input: &str) -> usize {
    // 2024 //    pII  III
    // track_len  156  340
    // plan_len    40   11
    // 156 % 40 = 36
    // 340 % 11 = 11
    //
    // XXX: every lap, the plan is shifted by 1 and repeat, so no need to run it 2024
    let laps = 11; // 2024

    let track = Track::parse(TRACK_3);
    let (_, essence_a) = track.run(input, laps, None)[0];

    let items = "+++++---===".chars().collect::<Vec<_>>();
    let mut count = 0;
    for item in items.permutations() {
        let item = item
            .iter()
            .map(ToString::to_string)
            .collect::<Vec<_>>()
            .join(",");
        let plan = format!("B:{item}");
        let (_, essence_b) = track.run(&plan, laps, Some(essence_a))[0];
        count += usize::from(essence_b > essence_a);
    }

    count
}

struct Plan {
    id: char,
    list: Vec<Action>,
}

impl Plan {
    fn from(line: &str) -> Self {
        let Some((id, plan)) = line.split_once(':') else {
            panic!();
        };

        Self {
            id: id.chars().next().unwrap(),
            list: plan
                .split(',')
                .map(|x| x.parse().unwrap())
                .collect::<Vec<_>>(),
        }
    }

    fn run(&self, end: usize) -> usize {
        let mut power = 10;
        let mut essence = 0;
        for i in 0..end {
            power = self.tick(power, i);
            essence += power;
        }
        essence
    }

    fn tick(&self, power: usize, i: usize) -> usize {
        match self.list[i % self.list.len()] {
            Action::Increase => power + 1,
            Action::Decrease if power > 0 => power - 1,
            _ => power,
        }
    }
}

struct Track(Vec<Action>);

impl Track {
    fn parse(s: &str) -> Self {
        let mut actions = Vec::new();
        actions.push(Action::Start);
        let mut grid: HashMap<(_, _), Action> = HashMap::new();
        for (row, line) in s.trim().lines().enumerate() {
            for (col, ch) in line.chars().enumerate() {
                if ch != ' ' {
                    grid.insert((col as isize, row as isize), ch.try_into().unwrap());
                }
            }
        }

        let dirs: [[(isize, isize); 3]; 4] = [
            /* right */ [(0, -1), (1, 0), (0, 1)],
            /* down  */ [(1, 0), (0, 1), (-1, 0)],
            /* left  */ [(0, 1), (-1, 0), (0, -1)],
            /* up    */ [(-1, 0), (0, -1), (1, 0)],
        ];

        let mut pos = (1, 0);
        let mut dir = 0;
        while pos != (0, 0) {
            actions.push(*grid.get(&pos).expect("position not found"));
            for (idx, d) in dirs[dir].iter().enumerate() {
                let n = (pos.0 + d.0, pos.1 + d.1);
                if grid.contains_key(&n) {
                    pos = n;
                    dir = (dir + idx + dirs.len() - 1) % dirs.len();
                    break;
                }
            }
        }

        Self(actions)
    }

    fn run(&self, input: &str, loops: usize, optimal: Option<usize>) -> Vec<(char, usize)> {
        input
            .trim()
            .lines()
            .map(Plan::from)
            .map(|plan| {
                let mut power = 10;
                let mut essence = 0;
                for i in 0..loops * self.len() {
                    match self.0[(i + 1) % self.len()] {
                        Action::Increase => power += 1,
                        Action::Decrease if power > 0 => power -= 1,
                        _ => power = plan.tick(power, i),
                    }
                    essence += power;
                    // trim a little
                    if optimal.is_some_and(|x| essence > x) {
                        break;
                    }
                }
                (plan.id, essence)
            })
            .collect()
    }

    const fn len(&self) -> usize {
        self.0.len()
    }
}

// why not?
trait Sorted {
    fn to_sorted(self) -> String;
}

impl Sorted for Vec<(char, usize)> {
    fn to_sorted(mut self) -> String {
        self.sort_by(|a, b| b.1.cmp(&a.1));
        self.iter().map(|(n, _)| *n).collect::<String>()
    }
}

#[derive(Clone, Copy)]
enum Action {
    Increase,
    Decrease,
    Maintain,
    Start,
}

impl FromStr for Action {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::try_from(s.chars().next().unwrap())
    }
}

impl TryFrom<char> for Action {
    type Error = String;

    fn try_from(ch: char) -> Result<Self, Self::Error> {
        Ok(match ch {
            '+' => Self::Increase,
            '-' => Self::Decrease,
            '=' => Self::Maintain,
            'S' => Self::Start,
            _ => panic!("invalid char: {ch}"),
        })
    }
}

#[cfg(test)]
mod test {
    use super::*;
    const EXAMPLE_1: &str = "
A:+,-,=,=
B:+,=,-,+
C:=,-,+,+
D:=,=,=,+";

    #[test]
    fn part1_example() {
        assert_eq!("BDCA", part1(EXAMPLE_1, 10));
    }

    #[test]
    fn part2_example() {
        let track = "
S+===
-   +
=+=-+";
        let track = Track::parse(track);
        let ranking = track.run(EXAMPLE_1, 10, None);
        assert_eq!("DCBA", ranking.to_sorted());
    }

    #[test]
    fn part3() {
        let track = "
S+= -=-
- + + -
- + + -
- -=+ +
-     -
=+=-+++";
        let track = Track::parse(track);
        let ranking = track.run(EXAMPLE_1, 10, None);
        assert_eq!(1810, ranking[0].1);
    }
}

const TRACK_2: &str = "
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-";

const TRACK_3: &str = "
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-";
