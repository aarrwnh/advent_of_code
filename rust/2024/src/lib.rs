pub mod d01;
pub mod d02;
pub mod d03;

// TOOD?
pub trait Solver {
    fn parse();

    fn part1();

    fn part2();

    fn solve(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}
