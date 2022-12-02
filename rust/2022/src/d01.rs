use std::{collections::BinaryHeap, fs::read_to_string, time::SystemTime};
use support::check_values;

fn get_calories(input: &str) -> impl Iterator<Item = u32> + '_ {
    return input.split("\n\n").map(|invertory: &str| {
        return invertory
            .lines()
            .flat_map(|calories| calories.parse::<u32>())
            .sum::<u32>();
    });
}

fn part1(input: &str) -> u32 {
    get_calories(input).max().unwrap()
}

fn part2(input: &str) -> u32 {
    // calories.sort_by(|a, b| b.cmp(a));
    get_calories(input)
        .collect::<BinaryHeap<u32>>()
        .iter()
        .take(3)
        .sum::<u32>()
}

pub fn main() {
    let sample = read_to_string("../input/2022/01/sample.input").unwrap();
    let puzzle = read_to_string("../input/2022/01/puzzle.input").unwrap();

    check_values!(24000, part1, &sample);
    check_values!(71924, part1, &puzzle);

    check_values!(45000, part2, &sample);
    check_values!(210406, part2, &puzzle);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(24000, part1(&sample()));
        assert_eq!(71924, part1(&puzzle()));
    }

    #[test]
    fn test_part2() {
        assert_eq!(45000, part2(&sample()));
        assert_eq!(210406, part2(&puzzle()));
    }

    fn sample() -> String {
        read_to_string("../../input/2022/01/sample.input").unwrap()
    }

    fn puzzle() -> String {
        read_to_string("../../input/2022/01/puzzle.input").unwrap()
    }
}
