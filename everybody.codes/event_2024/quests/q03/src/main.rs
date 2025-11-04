use std::collections::HashMap;

use utils::*;

fn main() {
    let input = InputReader::new("e2024", 3);
    check!(part1 <-   123 ; &input.load(1));
    check!(part2 <-  2663 ; &input.load(2));
    check!(part3 <- 10234 ; &input.load(3));
}

const DIRS: [(i64, i64); 4] = [(0, 1), (1, 0), (-1, 0), (0, -1)];
const DIRS_DIAG: [(i64, i64); 4] = [(1, 1), (1, -1), (-1, 1), (-1, -1)];

fn part1(input: &str) -> usize {
    Mine::from(input).dig_down(&DIRS)
}

fn part2(input: &str) -> usize {
    Mine::from(input).dig_down(&DIRS)
}

fn part3(input: &str) -> usize {
    Mine::from(input).dig_down(&[DIRS, DIRS_DIAG].concat())
}

struct Mine {
    grid: HashMap<(i64, i64), u8>,
    width: i64,
    height: i64,
}

impl Mine {
    fn from(input: &str) -> Self {
        let mut grid = HashMap::new();
        let (mut width, mut height) = (0, 0);
        for (row, line) in input.lines().enumerate() {
            for (col, ch) in line.chars().enumerate() {
                if ch != '.' {
                    grid.insert((col as i64, row as i64), 1);
                }
                width = width.max(col);
            }
            height = height.max(row);
        }
        Self {
            grid,
            height: height as i64,
            width: width as i64,
        }
    }

    fn dig_down(&mut self, dirs: &[(i64, i64)]) -> usize {
        let mut count = 0;
        let total = dirs.len();
        let check_adjacent = |g: &HashMap<_, _>, (c, r): &(i64, i64)| -> bool {
            dirs.iter()
                .map_while(|dir| g.get(&(c + dir.0, r + dir.1)))
                .count()
                == total
        };
        // let mut grid = &mut self.grid;
        while !self.grid.is_empty() {
            count += self.grid.len();
            // self._print();
            self.grid = self
                .grid
                .iter()
                .filter_map(|(p, lvl)| {
                    if check_adjacent(&self.grid, p) {
                        Some((*p, lvl + 1))
                    } else {
                        None
                    }
                })
                .collect::<_>();
        }
        count
    }

    fn _print(&self) {
        for r in 0..self.height {
            for c in 0..self.width {
                if let Some(p) = self.grid.get(&(c, r)) {
                    print!("{p}");
                } else {
                    print!(".");
                }
            }
            println!();
        }
        println!();
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part1_and_3_example() {
        let input = "
..........
..###.##..
...####...
..######..
..######..
...####...
..........";
        assert_eq!(35, Mine::from(input).dig_down(&DIRS));
        assert_eq!(29, Mine::from(input).dig_down(&[DIRS, DIRS_DIAG].concat()));
    }
}
