use std::collections::{HashMap, HashSet};

use support::{check, Grid, InputReader, Point};

const DIRS: [(i8, i8); 4] = [
    (0, -1), // ^
    (1, 0),  // >
    (0, 1),  // v
    (-1, 0), // <
];

enum Flow {
    Path(Box<dyn Iterator<Item = (isize, isize)>>),
    Loopin,
}

// slow?  debug: ~39s  release: ~3s  | python: 17s
fn walk(grid: &Grid, obstacle: Option<(isize, isize)>) -> Flow {
    let mut visited = HashSet::new();
    let Point(mut x, mut y) = grid.start();
    let mut dir = 0usize;
    let with_obstacle = obstacle.is_some();

    while grid.in_bounds(x, y) {
        let state = (if with_obstacle { dir } else { 0 }, x, y);
        if with_obstacle && visited.contains(&state) {
            return Flow::Loopin;
        }
        visited.insert(state);

        let (dx, dy) = DIRS[dir];
        let (mut nx, mut ny) = (x + dx as isize, y + dy as isize);

        if grid.in_bounds(nx, ny)
            && (grid.get((nx, ny).into()) == b'#' || obstacle.is_some_and(|p| p == (nx, ny)))
        {
            dir = (dir + 1) % 4;
        } else {
            (x, y) = (nx, ny)
        }
    }

    Flow::Path(Box::new(visited.into_iter().map(|x| (x.1, x.2))))
}

fn part1(grid: &Grid) -> usize {
    match walk(grid, None) {
        Flow::Path(path) => path.collect::<Vec<_>>().len(),
        _ => 0,
    }
}

fn part2(grid: &Grid) -> usize {
    if let Flow::Path(path) = walk(grid, None) {
        return path
            .into_iter()
            .filter_map(|x| match walk(grid, Some(x)) {
                Flow::Loopin => Some(1),
                _ => None,
            })
            .sum();
    }
    0
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 6);
    let start = Some(b'^');
    let e = Grid::from(&i.as_raw("example"), start);
    let p = Grid::from(&i.as_raw("puzzle"), start);

    check!("Part1" part1 [41 &e] [4977 &p]);
    check!("Part2" part2 [6 &e] [1729 &p]);

    Ok(())
}
