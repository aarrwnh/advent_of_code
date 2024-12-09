use std::collections::HashSet;

use support::{check, Grid, InputReader, Point};

fn find_antinodes(g: &Grid, start: isize, stop: isize) -> usize {
    let mut antennas = g.into_iter().filter(|x| *x.1 != b'.').collect::<Vec<_>>();
    let mut antinodes = HashSet::new();
    let mut check = |p: &Point, d: &Point| {
        let Point(x, y) = p;
        let Point(dx, dy) = d;
        for i in start..stop {
            let n = (x + dx * i, y + dy * i);
            if !g.in_bounds(n.0, n.1) {
                return;
            }
            antinodes.insert(n);
        }
    };
    while let Some((a1, p1)) = &antennas.pop() {
        for (a2, p2) in &antennas {
            if p1 == p2 {
                let d = a1.dist(a2);
                check(a1, &d);
                check(a2, &(-d.0, -d.1).into());
            }
        }
    }
    antinodes.len()
}

fn part1(g: &Grid) -> usize {
    find_antinodes(g, 1, 2)
}

fn part2(g: &Grid) -> usize {
    find_antinodes(g, 0, g.width())
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let i = InputReader::new(2024, 8);
    let e = Grid::from(&i.as_raw("example"), None);
    let p = Grid::from(&i.as_raw("puzzle"), None);

    check!("Part1" part1 [14 &e] [311 &p]);
    check!("Part2" part2 [34 &e] [1115 &p]);

    Ok(())
}
