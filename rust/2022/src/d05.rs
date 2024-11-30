use std::{error::Error, fs::read_to_string, time::SystemTime};

// fn parse_stack(raw_stack: &str) -> (HashMap<u8, Vec<String>>, std::str::Split<&str>) {
//     let (cargo, instructions) = raw_stack.split_once("\n\n").expect("should be two parts");
//     let cargo = cargo.split("\n").collect::<Vec<_>>();
//     let instructions = instructions.split("\n");

//     let mut stacks: HashMap<u8, Vec<String>> = HashMap::new();

//     for (i, line) in cargo.iter().enumerate() {
//         if i == cargo.len() - 1 || line.is_empty() {
//             break;
//         }

//         let mut i = -1;
//         let mut c = line.chars().collect::<Vec<char>>();
//         &c.retain(|&x| {
//             i += 1;
//             return i % 4 == 1;
//         });

//         for (j, ch) in (1..).zip(c).collect::<Vec<(u8, char)>>() {
//             let binding = ch.to_string();
//             if binding == " " {
//                 continue;
//             }
//             match stacks.get_mut(&j) {
//                 Some(stack) => {
//                     stack.push(binding);
//                 }
//                 _ => {
//                     stacks.insert(j, vec![binding]);
//                 }
//             };
//         }
//     }
//     (stacks, instructions)
// }

// fn parse(input: &str, insert_first: bool) -> String {
//     let (mut stacks, instructions) = parse_stack(input);

//     for inst in instructions {
//         if inst.is_empty() {
//             break;
//         }
//         let [_, amount, _, move_from, _, move_to] = inst.split(" ").collect::<Vec<&str>>()[..] else { todo!("")};
//         let amount: u8 = amount.parse().unwrap();
//         let move_from: u8 = move_from.parse().unwrap();
//         let move_to: u8 = move_to.parse().unwrap();

//         let mut removed: Vec<String> = Vec::new();
//         if let Some(from) = stacks.get_mut(&move_from) {
//             for removed_element in from.drain(0..(amount as usize)) {
//                 if insert_first {
//                     removed.insert(0, removed_element)
//                 } else {
//                     removed.push(removed_element)
//                 }
//             }
//         }

//         for r in removed {
//             if let Some(dest) = stacks.get_mut(&move_to) {
//                 dest.insert(0, r);
//             }
//         }
//     }

//     let mut output = Vec::new();
//     for s in 1..=stacks.keys().len() {
//         if let Some(v) = stacks.get_mut(&(s as u8)) {
//             output.push(v.first().unwrap().clone());
//         }
//     }

//     output.clone().join("")
// }

// fn part1(input: &str) -> String {
//     parse(input, false)
// }

// fn part2(input: &str) -> String {
//     parse(input, true)
// }

fn parse_stack(raw_stack: &str) -> (Vec<Vec<u8>>, std::str::Split<'_, &str>) {
    let (cargo_raw, instructions_raw) = raw_stack.split_once("\n\n").expect("should be two parts");
    let cargo_lines = cargo_raw.split("\n").collect::<Vec<_>>();
    let instructions = instructions_raw.split("\n");

    let line_size = (cargo_lines[0].len() + 1) as f32;
    let stocks_count = (line_size / 4.0).ceil() as usize;

    let mut stacks: Vec<Vec<u8>> = vec![vec![]; stocks_count + 1];

    for (i, line) in cargo_lines[..cargo_lines.len() - 1].iter().enumerate() {
        if line.is_empty() {
            break;
        }
        let mut j = 1;
        for (i, c) in line.as_bytes().iter().enumerate() {
            if i != 0 && i % 4 == 1 {
                if let Some(stack) = stacks.get(j) {
                    if *c != (32 as u8) {
                        stacks[j].push(*c);
                    }
                    j += 1;
                }
            }
        }
    }
    (stacks, instructions)
}

fn parse(input: &str, insert_first: bool) -> String {
    let (mut stacks, instructions) = parse_stack(input);

    for instr in instructions {
        if instr.is_empty() {
            continue;
        }

        let [amount, move_from, move_to] = instr
            .split(" ")
            .filter_map(|f| f.parse::<usize>().ok())
            .collect::<Vec<usize>>()[..] else { todo!("")};

        let mut removed: Vec<u8> = Vec::new();
        if let Some(from) = stacks.get_mut(move_from) {
            for removed_element in from.drain(0..amount) {
                if insert_first {
                    removed.insert(0, removed_element)
                } else {
                    removed.push(removed_element)
                }
            }
        }

        for r in removed {
            if let Some(dest) = stacks.get_mut(move_to) {
                dest.insert(0, r);
            }
        }
    }

    let mut output = String::new();
    for s in &stacks {
        if let Some(val) = s.first() {
            output.push(*val as char);
        }
    }

    stacks
        .into_iter()
        .filter_map(move |f| match f.first() {
            Some(val) => Some(*val as char),
            None => None, // ignore empty array at index 0
        })
        .collect::<String>()
}

fn part1(input: &str) -> String {
    parse(input, false)
}

fn part2(input: &str) -> String {
    parse(input, true)
}

pub fn main() -> Result<(), Box<dyn Error>> {
    let sample: String = read_to_string("../input/2022/05/sample.input")?.parse()?;
    let puzzle: String = read_to_string("../input/2022/05/puzzle.input")?.parse()?;

    // check_values!("CMZ", part1, &sample);
    // check_values!("HNSNMTLHQ", part1, &puzzle);

    // check_values!("MCD", part2, &sample);
    // check_values!("RNLFDJMCT", part2, &puzzle);

    Ok(())
}
