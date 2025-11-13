use utils::*;

fn main() {
    let input = InputReader::new("e2025", 6);
    check!(part1 <-        178 ; &input.load(1));
    check!(part2 <-       4566 ; &input.load(2));
    check!(part3 <- 1665346942 ; &input.load(3), 1000, 1000);
}

fn part1(input: &str) -> usize {
    // let mut total = 0;
    // let mut mentors = 0;
    // for ch in input.trim().chars() {
    //     match ch {
    //         'A' => mentors += 1,
    //         'a' => total += mentors,
    //         _ => {}
    //     }
    // }
    // total
    count_pairs(input.as_bytes())[0]
}

fn part2(input: &str) -> usize {
    // count_pairs(input.as_bytes()).iter().sum()
    counter(input.as_bytes(), 1, input.len())
}

fn part3(input: &str, repeats: usize, distance: usize) -> usize {
    // let count = |input: &str| {
    //     let mut total = 0;
    //     for (i, ch) in input.chars().enumerate() {
    //         if ch.is_ascii_lowercase() {
    //             let start = 0.max(i as i64 - distance as i64) as usize;
    //             let end = input.len().min(i + distance + 1);
    //             let n = ch.to_ascii_uppercase();
    //             for c in input[start..end].chars() {
    //                 if c == n {
    //                     total += 1;
    //                 }
    //             }
    //         }
    //     }
    //     total
    // };

    // assert!(repeats > 1);
    // let input = input.trim();
    // let a = count(&input);
    // let b = count(&input.repeat(2));
    // a + ((b - a) * (repeats - 1))

    let input = input.trim().as_bytes();
    let a = counter(input, repeats, distance);
    let rev = input.iter().copied().rev().collect::<Vec<_>>();
    let b = counter(&rev, repeats, distance);
    a + b
}

fn count_pairs(chars: &[u8]) -> Vec<usize> {
    let mut total = vec![0usize; 3];
    let mut counts = vec![0usize; 3];
    for ch in chars {
        if ch.is_ascii_uppercase() {
            counts[(ch - b'A') as usize] += 1;
        } else {
            let i = (ch - b'a') as usize;
            total[i] += counts[i];
        }
    }
    total
}

fn counter(chars: &[u8], repeats: usize, distance: usize) -> usize {
    let mut total = 0;

    // keep track of mentors position within the range
    // (assume we only need 3 keys (ABC))
    // let mut counts: Vec<VecDeque<usize>> = vec![VecDeque::new(); 3];
    let mut counts: Vec<usize> = vec![0; 3];
    let mut idx = 0usize;

    for rep in 0..repeats {
        let mut current_total = 0;
        for ch in chars {
            if ch.is_ascii_uppercase() {
                counts[(ch - b'A') as usize] += 1;
            } else {
                // prune mentors outside of the range
                // while let Some(m_idx) = counts[key].front() {
                //     if idx - m_idx > distance {
                //         counts[key].pop_front();
                //     } else {
                //         break;
                //     }
                // }

                let key = (ch - b'a') as usize;
                current_total += counts[key];
            }

            if let Some(d) = idx.checked_sub(distance) {
                let p = d % chars.len();
                if chars[p].is_ascii_uppercase() {
                    counts[(chars[p] - b'A') as usize] -= 1;
                }
            }

            idx += 1;
        }

        if rep * chars.len() > distance as usize {
            total += current_total * (repeats - rep);
            break;
        } else {
            total += current_total
        }
    }

    total
}

#[cfg(test)]
mod q06 {
    use super::*;
    const INPUT1: &str = "ABabACacBCbca";
    const INPUT2: &str = "AABCBABCABCabcabcABCCBAACBCa";

    #[test]
    fn part1_example() {
        assert_eq!(5, part1(INPUT1));
    }

    #[test]
    fn part2_example() {
        assert_eq!(11, part2(INPUT1));
    }

    #[test]
    fn part3_example() {
        assert_eq!(34, part3(INPUT2, 1, 10));
        assert_eq!(72, part3(INPUT2, 2, 10));
        assert_eq!(3442321, part3(INPUT2, 1000, 1000));
    }
}
