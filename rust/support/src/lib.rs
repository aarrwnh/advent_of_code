mod macros;

use std::{collections::HashMap, str::FromStr};

pub use crate::macros::*;

#[derive(Debug, Default)]
pub struct InputReader(String);

impl InputReader {
    pub fn new(year: usize, day: usize) -> Self {
        Self(format!("../../input/{year}/{day:0>2}-"))
    }

    fn _get_file(&self, filename: &str) -> String {
        ::std::fs::read_to_string(self.0.clone() + filename).expect("unable to open file")
    }

    pub fn as_raw(&self, filename: &str) -> String {
        self._get_file(filename)
    }

    pub fn as_chars(&self, filename: &str) -> Vec<char> {
        self._get_file(filename).chars().collect()
    }
}

#[derive(Hash, Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct Point(pub isize, pub isize);

impl Point {
    pub fn dist(&self, other: &Self) -> Self {
        (self.0 - other.0, self.1 - other.1).into()
    }

    pub fn apply(&self, other: &Self) -> Self {
        (self.0 + other.0, self.1 + other.1).into()
    }
}

impl From<(isize, isize)> for Point {
    fn from(e: (isize, isize)) -> Self {
        Self(e.0, e.1)
    }
}

#[derive(Debug)]
pub struct Grid {
    pub points: HashMap<Point, u8>,
    pub max_x: isize,
    pub max_y: isize,
    pub start_pos: Option<Point>,
}

impl FromStr for Grid {
    type Err = Box<dyn std::error::Error>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Grid::from(s, None))
    }
}

impl Grid {
    pub fn from(input: &str, start_ch: Option<u8>) -> Self {
        let mut map = HashMap::new();
        let mut max_x = 0;
        let mut max_y = 0;

        for (y, line) in input.lines().enumerate() {
            for (x, ch) in line.chars().enumerate() {
                map.insert((x as isize, y as isize).into(), ch as u8);
                max_x = x as isize;
            }
            max_y = y as isize;
        }

        let start_pos = match start_ch {
            Some(ch) => map
                .iter()
                .find_map(|(k, v)| if *v == ch { Some(*k) } else { None }),
            None => None,
        };

        Self {
            points: map,
            max_x,
            max_y,
            start_pos,
        }
    }

    pub fn start(&self) -> Point {
        self.start_pos.expect("grid entrypoint")
    }

    pub fn in_bounds(&self, x: isize, y: isize) -> bool {
        // x <= 0 && x <= self.max_x && y <= 0 && y <= self.max_y
        (0..=self.max_x).contains(&x) && (0..=self.max_y).contains(&y)
    }

    pub fn width(&self) -> isize {
        self.max_x + 1
    }

    pub fn height(&self) -> isize {
        self.max_y + 1
    }

    pub fn get(&self, k: Point) -> u8 {
        self.points.get(&k).copied().unwrap()
    }
}

impl<'a> IntoIterator for &'a Grid {
    type Item = <&'a HashMap<Point, u8> as IntoIterator>::Item;
    type IntoIter = <&'a HashMap<Point, u8> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.points.iter()
    }
}
