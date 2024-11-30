mod macros;

pub use crate::macros::*;

#[derive(Debug, Default)]
pub struct InputReader(String);

impl InputReader {
    pub fn new(year: usize, day: usize) -> Self {
        Self(format!("../input/{year}/{day:0>2}/"))
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
