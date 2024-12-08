use std::collections::HashSet;

use support::{check, Grid, InputReader};

const DIRS: [(i8, i8); 4] = [
    (0, -1), // ^
    (1, 0),  // >
    (0, 1),  // v
    (-1, 0), // <
];

fn advance(dir: u8, x: isize, y: isize) -> (isize, isize) {
    let (dx, dy) = DIRS[dir as usize];
    (x.wrapping_add(dx.into()), y.wrapping_add(dy.into()))
}

enum Flow {
    Path(Box<dyn Iterator<Item = (isize, isize)>>),
    Loopin,
}

// slow?  debug: ~39s  release: ~4s  | python: 17s
fn walk(grid: &Grid, obstacle: Option<(isize, isize)>) -> Flow {
    let mut visited = HashSet::new();
    let (mut x, mut y) = grid.start();
    let mut dir = 0;
    let with_obstacle = obstacle.is_some();

    while grid.in_bounds(x, y) {
        let state = (if with_obstacle { dir } else { 0 }, x, y);
        if with_obstacle && visited.contains(&state) {
            return Flow::Loopin;
        }
        visited.insert(state);
        let (mut nx, mut ny) = advance(dir, x, y);

        while grid.in_bounds(nx, ny)
            && (*grid.points.get(&(nx, ny)).unwrap() == b'#'
                || obstacle.is_some_and(|p| p == (nx, ny)))
        {
            dir = (dir + 1) % 4;
            (nx, ny) = advance(dir, x, y);
        }

        (x, y) = (nx, ny)
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
