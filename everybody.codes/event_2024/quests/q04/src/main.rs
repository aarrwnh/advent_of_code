use utils::*;

fn main() {
    let input = InputReader::new("e2024", 4);
    check!(part1 <-        76 ; &input.load(1));
    check!(part2 <-    855525 ; &input.load(2));
    check!(part3 <- 122238609 ; &input.load(3));
}

fn part1(input: &str) -> u64 {
    level_nails(input)
}

fn part2(input: &str) -> u64 {
    level_nails(input)
}

fn part3(input: &str) -> u64 {
    level_nails_optimal(input)
}

fn parse(input: &str) -> Vec<u64> {
    input
        .lines()
        .map(|x| x.parse::<u64>().expect("integer could not be parsed"))
        .collect()
}

fn level_nails(input: &str) -> u64 {
    let mut nails = parse(input);
    assert!(nails.len() > 1);
    nails.sort();
    let min = nails[0];
    nails
        .iter()
        .map(|n| if *n > min { n - min } else { 0 })
        .sum()
}

fn level_nails_optimal(input: &str) -> u64 {
    let nails = parse(input);
    assert!(nails.len() > 1);
    let mut optimal = u64::MAX;
    for min in &nails {
        optimal = optimal.min(
            nails
                .iter()
                .map(|n| if *n > *min { n - *min } else { *min - n })
                .sum(),
        );
    }
    optimal
}
