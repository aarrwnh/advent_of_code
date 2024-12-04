use std::{cmp::Ordering::Equal, collections::HashMap};

use support::{check, InputReader};

type Coord = isize;
type P = (Coord, Coord);
type Grid = HashMap<P, char>;

const DIRS_4: [P; 4] = [
    (0, 1),  // up
    (0, -1), // down
    (1, 0),  // right
    (-1, 0), // left
];

const DIRS_DIAG: [P; 4] = [
    (1, 1),   // top-right
    (-1, -1), // bottom-left
    (-1, 1),  // top-left
    (1, -1),  // bottom-right
];

fn traverse(x: Coord, y: Coord, r: isize, dirs: &[P], mut f: impl FnMut(bool, Coord, Coord)) {
    dirs.iter().for_each(|(dx, dy)| {
        (1..=r).for_each(|i| f(i % r == 0, x + dx * i, y + dy * i));
    });
}

fn parse(input: &str) -> Grid {
    let mut grid: Grid = HashMap::new();
    let lines = input.lines().collect::<Vec<_>>();
    lines.iter().enumerate().for_each(|(y, row)| {
        row.chars().enumerate().for_each(|(x, p)| {
            grid.insert((x as Coord, y as Coord), p);
        });
    });
    grid
}

fn part1(grid: &Grid) -> u64 {
    let dirs: [P; 8] = [&DIRS_DIAG[..], &DIRS_4].concat().try_into().unwrap();
    let (max_x, max_y) = grid.keys().max().unwrap();
    let mut total = 0;
    let templ = vec!['M', 'A', 'S'];
    let word_size = 4; // XMAS
    let mut word = Vec::with_capacity(word_size as usize - 1);
    grid.keys().for_each(|n| {
        let ch = grid.get(n).unwrap();
        if *ch != 'X' {
            return;
        }
        traverse(n.0, n.1, word_size, &dirs, |reset, dx, dy| {
            if reset {
                if word.cmp(&templ) == Equal {
                    total += 1;
                }
                return word.clear();
            }
            if !(dx >= 0 && dx <= *max_x && dy >= 0 && dy <= *max_y) {
                return;
            }
            word.push(*grid.get(&(dx, dy)).unwrap());
        });
    });
    total
}

fn part2(grid: &Grid) -> u64 {
    let (max_x, max_y) = grid.keys().max().unwrap();
    let mut total = 0;
    let templ = ['A', 'S'];
    let word_size = 3; // MAS
    let mut counter = HashMap::new();
    let mut found = Vec::with_capacity(word_size as usize - 1);
    grid.keys().for_each(|n| {
        let ch = grid.get(n).unwrap();
        if *ch != 'M' {
            return;
        }
        traverse(n.0, n.1, word_size, &DIRS_DIAG, |reset, dx, dy| {
            if reset {
                let w = found.iter().map(|p| grid.get(p).unwrap());
                if w.cmp(&templ) == Equal {
                    let p = found[0];
                    let c = counter.entry(p).or_insert(1);
                    if *c == 2 && grid[&p] == 'A' {
                        total += 1;
                    }
                    *c += 1;
                }
                return found.clear();
            }
            if !(dx >= 0 && dx <= *max_x && dy >= 0 && dy <= *max_y) {
                return;
            }
            found.push((dx, dy));
        });
    });
    total
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 4);
    let e = parse(&i.as_raw("example"));
    let p = parse(&i.as_raw("puzzle"));

    check!("Part1" part1 [18 &e] [2336 &p]);
    check!("Part2" part2 [9 &e] [1831 &p]);

    Ok(())
}
