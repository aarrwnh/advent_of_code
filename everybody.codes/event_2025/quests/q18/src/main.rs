use std::{collections::HashMap, str::FromStr};

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 18);
    check!(part1 <-     2868456 ; &input.load(1));
    check!(part2 <- 15144285134 ; &input.load(2));
    check!(part3 <-      223710 ; &input.load(3));
}

fn part1(input: &str) -> usize {
    Plants::from_str(input).unwrap().calc_energy(None)
}

fn part2(input: &str) -> usize {
    let plants = Plants::from_str(input).unwrap();
    let Some(test_cases) = plants.test_cases.as_ref() else {
        panic!();
    };
    test_cases
        .iter()
        .map(|tc| plants.calc_energy(Some(tc)))
        .sum()
}

fn part3(input: &str) -> usize {
    // because of how input puzzle is structured we can just assume things
    // about the structure, but example needs to find correct combination instead
    //
    // 81 free branches on layer 1
    // we check if connections on layer 2 are either positive(1) or neg(0)
    find_optimal(input, |plants| {
        let mut optimal = vec![0u8; plants.offset];
        for (_, plant) in &plants.plants {
            let (thic, linked) = plant;
            for &Plant { id, thickness } in linked.iter() {
                let id = id as usize;
                // using 0 for free branches
                if id > 0 && id <= plants.offset && thickness > 0 {
                    optimal[id - 1] = 1;
                }
            }
        }

        plants.calc_energy(Some(&optimal))
    })
}

fn find_optimal(input: &str, cb: fn(plants: &Plants) -> usize) -> usize {
    let plants = Plants::from_str(input).unwrap();
    let Some(test_cases) = plants.test_cases.as_ref() else {
        panic!();
    };

    let best = cb(&plants);

    test_cases
        .iter()
        .map(|tc| {
            let res = plants.calc_energy(Some(tc));
            if res > 0 && res < best { best - res } else { 0 }
        })
        .sum()
}

#[derive(Debug)]
struct Plant {
    id: isize,
    thickness: isize,
}

impl Plant {
    fn new(id: &str, thick: &str) -> Self {
        Self {
            id: parse(id),
            thickness: parse(thick),
        }
    }

    fn free(thick: &str) -> Self {
        Self {
            id: 0,
            thickness: parse(thick),
        }
    }
}

fn parse<T>(n: &str) -> T
where
    T: FromStr,
    <T as FromStr>::Err: std::fmt::Debug,
{
    n.parse::<T>().unwrap()
}

#[derive(Debug)]
struct Plants {
    plants: HashMap<isize, (isize, Vec<Plant>)>,
    test_cases: Option<Vec<Vec<u8>>>,
    offset: usize,
}

impl FromStr for Plants {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let input = s.trim();
        let (plants, test_cases) = if input.contains("\n\n\n") {
            let (a, b) = input.split_once("\n\n\n").unwrap();
            let b = b
                .lines()
                .map(|line| line.split(' ').map(|n| parse(n)).collect::<Vec<_>>())
                .collect::<Vec<_>>();
            (a, Some(b))
        } else {
            (input, None)
        };

        let mut free_offset = 0;
        let plants = plants
            .split("\n\n")
            .map(|s| {
                let lines = s.lines().collect::<Vec<_>>();
                let [_, id, _, _, thickness] = lines[0][0..lines[0].len() - 1]
                    .split(' ')
                    .collect::<Vec<_>>()[..]
                else {
                    panic!()
                };

                let mut branches = Vec::new();
                for n in lines.iter().skip(1) {
                    let p = n.split(' ').collect::<Vec<_>>();
                    if p[1] == "free" {
                        free_offset += 1;
                        // println!("start -> plant{id};");
                        branches.push(Plant::free(p[5]))
                    } else {
                        // println!("plant{} -> plant{id};", p[4]);
                        branches.push(Plant::new(p[4], p[7]));
                    }
                }

                (parse(id), (parse(thickness), branches))
            })
            .collect::<HashMap<_, _>>();

        Ok(Self {
            plants,
            test_cases,
            offset: free_offset,
        })
    }
}

impl Plants {
    fn calc_energy(&self, test_case: Option<&[u8]>) -> usize {
        let mut map: HashMap<isize, isize> = HashMap::new();
        let mut start = 1; // plant id

        // if avaliable use test case to fill initial values
        if let Some(tc) = test_case {
            start += tc.len() as isize;
            for (i, &e) in (1..).zip(tc.iter()) {
                map.insert(i, e as isize);
            }
        }

        let count = self.plants.len() as isize;
        for plant in start..=count {
            let (thic, branches) = &self.plants[&plant];

            let energy = branches
                .iter()
                .map(|p| *map.entry(p.id).or_insert(1) * p.thickness)
                .sum::<isize>();

            let v = map.entry(plant).or_insert(energy);
            if *v < *thic {
                *v = 0;
            }
        }
        map[&count] as usize
    }
}

#[cfg(test)]
mod q18 {
    use super::*;

    #[test]
    fn part1_example() {
        let s = "
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 17:
- branch to Plant 1 with thickness 15
- branch to Plant 2 with thickness 3

Plant 5 with thickness 24:
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13

Plant 6 with thickness 15:
- branch to Plant 3 with thickness 14

Plant 7 with thickness 10:
- branch to Plant 4 with thickness 15
- branch to Plant 5 with thickness 21
- branch to Plant 6 with thickness 34";
        assert_eq!(774, part1(s));
    }

    #[test]
    fn part2_example() {
        let s = "
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 10:
- branch to Plant 1 with thickness -25
- branch to Plant 2 with thickness 17
- branch to Plant 3 with thickness 12

Plant 5 with thickness 14:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -26
- branch to Plant 3 with thickness 15

Plant 6 with thickness 150:
- branch to Plant 4 with thickness 5
- branch to Plant 5 with thickness 6


1 0 1
0 0 1
0 1 1";
        assert_eq!(324, part2(s));
    }

    #[test]
    fn part3_example() {
        let s = "
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 1:
- free branch with thickness 1

Plant 5 with thickness 8:
- branch to Plant 1 with thickness -8
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13
- branch to Plant 4 with thickness -7

Plant 6 with thickness 7:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -9
- branch to Plant 3 with thickness 12
- branch to Plant 4 with thickness 9

Plant 7 with thickness 23:
- branch to Plant 5 with thickness 17
- branch to Plant 6 with thickness 18


0 1 0 0
0 1 0 1
0 1 1 1
1 1 0 1";

        assert_eq!(
            946,
            find_optimal(s, |plants| {
                cproduct([0, 1], plants.offset)
                    .iter()
                    .map(|tc| plants.calc_energy(Some(&tc)))
                    .max()
                    .unwrap()
            })
        );
    }

    fn cproduct<const N: usize, T: Clone>(iter: [T; N], repeat: usize) -> Vec<Vec<T>> {
        assert!(repeat < 5 && N < 5);
        let pools = [&iter].repeat(repeat);
        let mut result = vec![vec![]];
        for pool in pools.into_iter() {
            result = result
                .into_iter()
                .flat_map(|x| {
                    pool.iter()
                        .cloned()
                        .map(|y| {
                            let mut x = x.clone();
                            x.push(y);
                            x
                        })
                        .collect::<Vec<_>>()
                })
                .collect::<Vec<_>>();
        }
        result
    }
}
