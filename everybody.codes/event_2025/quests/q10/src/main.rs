use std::{
    collections::{HashMap, HashSet},
    str::FromStr,
};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 10);
    check!(part1 <-            153 ; &input.load(1), 4);
    check!(part2 <-           1688 ; &input.load(2), 20);
    check!(part3 <- 27199021009165 ; &input.load(3));
}

fn part1(input: &str, moves: usize) -> usize {
    let cb = Chessboard::from_str(input).unwrap();
    cb.run(moves, |visited| cb.count_sheep(&visited), |_, _| {})
}

fn part2(input: &str, rounds: usize) -> usize {
    let cb = Chessboard::from_str(input).unwrap();
    let sheeps = cb.get_sheeps();
    let mut eaats = vec![0; sheeps.len()];
    cb.run(
        rounds,
        |_| 0, // ignored
        |visited, round| {
            for (i, pos) in sheeps.iter().enumerate() {
                if eaats[i] == 1 {
                    continue;
                }
                let pos = (pos.0 + (round as isize * 1), pos.1);
                if pos.0 + 1 > cb.max_row {
                    continue;
                }
                let n = (pos.0 + 1, pos.1);
                if [n, pos]
                    .iter()
                    .any(|x| visited.contains(&x) && !cb.is_hideout(&x))
                {
                    eaats[i] = 1;
                }
            }
            visited.clear();
        },
    );
    eaats.iter().sum::<usize>()
}

fn part3(input: &str) -> usize {
    let cb = Chessboard::from_str(input).unwrap();
    let dragon = cb.get_dragon();
    let sheeps = cb.get_sheeps();
    let mut counter = cb.into_counter();
    counter.sheep_turn(dragon, sheeps)
}

#[derive(Eq, PartialEq, Hash)]
enum Turn {
    Dragon,
    Sheep,
}

struct Counter<'a> {
    cache: HashMap<(Turn, Position, Vec<Position>), usize>,
    max_row: isize,
    max_col: isize,
    grid: &'a HashMap<(isize, isize), Symbol>,
}

impl Counter<'_> {
    fn is_hideout(&self, pos: &Position) -> bool {
        self.grid.get(pos).is_some_and(|ch| *ch == Symbol::Hideout)
    }

    fn sheep_turn(&mut self, dragon: Position, sheeps: Vec<Position>) -> usize {
        if let Some(&v) = self.cache.get(&(Turn::Sheep, dragon, sheeps.to_vec())) {
            return v;
        }

        let mut total = 0;

        if sheeps.len() == 0 {
            total = 1;
        } else {
            let mut moved = 0;
            for (i, &(sr, sc)) in sheeps.iter().enumerate() {
                if sr == self.max_row {
                    moved += 1;
                } else if self.is_hideout(&(sr + 1, sc)) || dragon != (sr + 1, sc) {
                    moved += 1;
                    let sheeps = sheeps
                        .iter()
                        .enumerate()
                        .map(|(j, &(sr, sc))| if i == j { (sr + 1, sc) } else { (sr, sc) })
                        .collect();
                    total += self.dragon_turn(dragon, sheeps)
                }
            }
            if moved == 0 {
                total += self.dragon_turn(dragon, sheeps.to_vec());
            }
        }

        self.cache
            .insert((Turn::Sheep, dragon, sheeps.to_vec()), total);
        total
    }

    fn dragon_turn(&mut self, dragon: Position, sheeps: Vec<Position>) -> usize {
        if let Some(&v) = self.cache.get(&(Turn::Dragon, dragon, sheeps.to_vec())) {
            return v;
        }

        let mut total = 0;

        for n in Chessboard::next_moves(dragon.0, dragon.1, self.max_row, self.max_col) {
            let sheeps = sheeps
                .iter()
                .filter_map(|&s| {
                    if self.grid.get(&s).is_some_and(|&ch| ch == Symbol::Hideout) || s != n {
                        Some(s)
                    } else {
                        None
                    }
                })
                .collect();
            total += self.sheep_turn(n, sheeps);
        }

        self.cache
            .insert((Turn::Dragon, dragon, sheeps.to_vec()), total);
        total
    }
}

struct Chessboard {
    grid: HashMap<Position, Symbol>,
    max_row: isize,
    max_col: isize,
}

impl FromStr for Chessboard {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut grid = HashMap::new();
        let mut max_row = 0;
        let mut max_col = 0;
        for (row, line) in s.trim().lines().enumerate() {
            for (col, ch) in line.chars().enumerate() {
                if ch != '.' {
                    grid.insert((row as isize, col as isize), ch.into());
                }
                max_col = col;
            }
            max_row = row;
        }
        Ok(Self {
            grid,
            max_row: max_row as isize,
            max_col: max_col as isize,
        })
    }
}

type Position = (isize, isize);

impl Chessboard {
    fn into_counter(&'_ self) -> Counter<'_> {
        Counter {
            cache: HashMap::new(),
            grid: &self.grid,
            max_col: self.max_col,
            max_row: self.max_row,
        }
    }

    fn get_dragon(&self) -> Position {
        if let Some(dragon) = self.grid.iter().find(|(_, ch)| **ch == Symbol::Dragon) {
            *dragon.0
        } else {
            panic!()
        }
    }

    fn get_sheeps(&self) -> Vec<Position> {
        self.grid
            .iter()
            .filter(|(_, ch)| **ch == Symbol::Sheep)
            .map(|x| *x.0)
            .collect::<Vec<_>>()
    }

    fn is_hideout(&self, pos: &Position) -> bool {
        self.grid.get(pos).is_some_and(|ch| *ch == Symbol::Hideout)
    }

    fn next_moves(
        row: isize,
        col: isize,
        max_row: isize,
        max_col: isize,
    ) -> impl Iterator<Item = Position> {
        [
            (-1isize, -2isize),
            (-2, -1),
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
        ]
        .iter()
        .filter_map(move |(dy, dx)| {
            let a = row + dy;
            let b = col + dx;
            if 0 <= a && a <= max_row && 0 <= b && b <= max_col {
                Some((a, b))
            } else {
                None
            }
        })
    }

    fn count_sheep(&self, visited: &HashSet<Position>) -> usize {
        self.grid
            .iter()
            .filter(|(pos, ch)| **ch == Symbol::Sheep && visited.contains(pos))
            .count()
    }

    fn run(
        &self,
        moves: usize,
        mut done: impl FnMut(&HashSet<Position>) -> usize,
        mut tick: impl FnMut(&mut HashSet<Position>, usize),
    ) -> usize {
        let dragon = self.get_dragon();
        let mut queue = Vec::from([dragon]);
        let mut visited = HashSet::from([dragon]);

        for idx in 0..moves {
            let mut cand = Vec::new();
            while let Some((row, col)) = queue.pop() {
                for n in Chessboard::next_moves(row, col, self.max_row, self.max_col) {
                    if !visited.insert(n) {
                        continue;
                    }
                    cand.push(n);
                }
            }
            tick(&mut visited, idx);
            queue = cand;

            // for y in 0..20 {
            //     for x in 0..20 {
            //         if visited.contains(&(y, x)) {
            //             print!("X");
            //         } else {
            //             print!(".");
            //         }
            //     }
            //     println!()
            // }
        }

        done(&visited)
    }
}

#[derive(PartialEq, Eq, Clone, Copy)]
enum Symbol {
    Sheep,
    Dragon,
    Hideout,
}

impl From<char> for Symbol {
    fn from(e: char) -> Self {
        match e {
            'S' => Self::Sheep,
            'D' => Self::Dragon,
            '#' => Self::Hideout,
            _ => panic!(),
        }
    }
}

#[cfg(test)]
mod q10 {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "
...SSS.......
.S......S.SS.
..S....S...S.
..........SS.
..SSSS...S...
.....SS..S..S
SS....D.S....
S.S..S..S....
....S.......S
.SSS..SS.....
.........S...
.......S....S
SS.....S..S..";
        assert_eq!(27, part1(input, 3));
    }

    #[test]
    fn part2_example() {
        let input = "
...SSS##.....
.S#.##..S#SS.
..S.##.S#..S.
.#..#S##..SS.
..SSSS.#.S.#.
.##..SS.#S.#S
SS##.#D.S.#..
S.S..S..S###.
.##.S#.#....S
.SSS.#SS..##.
..#.##...S##.
.#...#.S#...S
SS...#.S.#S..";
        assert_eq!(27, part2(input, 3));
    }

    #[test]
    fn part3_example() {
        let input1 = "SSS\n..#\n#.#\n#D.";
        let input2 = "SSS\n..#\n..#\n.##\n.D#";
        let input3 = "..S..\n.....\n..#..\n.....\n..D..";
        let input4 = ".SS.S\n#...#\n...#.\n##..#\n.####\n##D.#";
        let input5 = "SSS.S\n.....\n#.#.#\n.#.#.\n#.D.#";
        assert_eq!(15, part3(input1));
        assert_eq!(8, part3(input2));
        assert_eq!(44, part3(input3));
        assert_eq!(4406, part3(input4));
        assert_eq!(13033988838, part3(input5));
    }
}
