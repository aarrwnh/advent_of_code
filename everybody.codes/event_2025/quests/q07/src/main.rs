use std::collections::HashMap;

use utils::*;

fn main() {
    let input = InputReader::new("e2025", 7);
    check!(part1 <- "Nyendris" ; &input.load(1));
    check!(part2 <-       2743 ; &input.load(2));
    check!(part3 <-    1674696 ; &input.load(3));
}

fn part1(input: &str) -> String {
    let (names, rules) = parse(input);
    let names = names
        .iter()
        .filter(|name| is_valid(name, &rules))
        .collect::<Vec<_>>();
    assert!(names.len() == 1);
    str::from_utf8(names[0]).unwrap().to_string()
}

fn part2(input: &str) -> usize {
    let (names, rules) = parse(input);
    names
        .iter()
        .enumerate()
        .filter_map(|(i, name)| {
            if is_valid(name, &rules) {
                Some(i + 1)
            } else {
                None
            }
        })
        .sum()
}

fn part3(input: &str) -> usize {
    let (names, rules) = parse(input);
    // let mut seen = HashSet::new();
    names
        .iter()
        .filter(|prefix| is_valid(prefix, &rules))
        .fold(Box::new(&mut Vec::new()), |out, prefix| {
            // also filter: Ny,Nyl,Nyth,Nyss -> Ny
            if !out.iter().copied().any(|x| prefix.starts_with(x)) {
                out.push(prefix);
            }
            out
        })
        .into_iter()
        .map(|prefix| count_unique(*prefix.last().unwrap(), prefix.len(), &rules))
        .sum()
}

fn count_unique(last: u8, length: usize, rules: &HashMap<u8, Vec<u8>>) -> usize {
    let mut result = (length >= 7) as usize;
    if length < 11
        && let Some(arr) = rules.get(&last)
    {
        for n in arr {
            result += count_unique(*n, length + 1, rules);
        }
    }
    result
}

// fn count_unique(
//     prefix: &mut Vec<u8>,
//     rules: &HashMap<u8, Vec<u8>>,
//     seen: &mut HashSet<Vec<u8>>,
// ) -> usize {
//     if prefix.len() == 7 && !seen.insert(prefix.clone()) {
//         return 0;
//     }
//     let mut result = (prefix.len() >= 7) as usize;
//     if prefix.len() < 11
//         && let Some(arr) = rules.get(prefix.last().unwrap())
//     {
//         for n in arr {
//             prefix.push(*n);
//             result += count_unique(prefix, rules, seen);
//             prefix.pop();
//         }
//     }
//     result
// }

fn is_valid(name: &[u8], rules: &HashMap<u8, Vec<u8>>) -> bool {
    name.windows(2).all(|pair| {
        rules
            .get(&pair[0])
            .is_some_and(|arr| arr.contains(&pair[1]))
    })
}

fn parse(input: &str) -> (Vec<&[u8]>, HashMap<u8, Vec<u8>>) {
    let (names, rules) = input.trim().split_once("\n\n").unwrap();
    let names = names.split(',').map(str::as_bytes).collect();
    let rules = rules
        .lines()
        .filter_map(|line| {
            let (left, right) = line.split_once(" > ")?;
            Some((
                *left.as_bytes().first()?,
                right
                    .split(',')
                    .map(|x| *x.as_bytes().first().unwrap())
                    .collect(),
            ))
        })
        .collect();
    (names, rules)
}

#[cfg(test)]
mod q07 {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "Oronris,Urakris,Oroneth,Uraketh

r > a,i,o
i > p,w
n > e,r
o > n,m
k > f,r
a > k
U > r
e > t
O > r
t > h";
        assert_eq!("Oroneth", part1(input));
    }

    #[test]
    fn part2_example() {
        let input = "Xanverax,Khargyth,Nexzeth,Helther,Braerex,Tirgryph,Kharverax

r > v,e,a,g,y
a > e,v,x,r
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i";
        assert_eq!(23, part2(input));
    }

    #[test]
    fn part3_example1() {
        let input = "Xaryt

X > a,o
a > r,t
r > y,e,a
h > a,e,v
t > h
v > e
y > p,t";
        assert_eq!(25, part3(input));
    }

    #[test]
    fn part3_example2() {
        let input = "Khara,Xaryt,Noxer,Kharax

r > v,e,a,g,y
a > e,v,x,r,g
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i";
        assert_eq!(1154, part3(input));
    }
}
