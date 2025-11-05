use std::ops::{Add, AddAssign, Div, DivAssign, Mul, MulAssign};

#[cfg(feature = "visualize")]
mod pallette;
#[cfg(feature = "visualize")]
use pallette::Palette;

use utils::*;

// https://en.wikipedia.org/wiki/Mandelbrot_set

fn main() {
    let input = InputReader::new("e2025", 2);
    check!(part1 <- "[261550,924584]" ; &input.load(1));
    check!(part2 <-               651 ; &input.load(2));
    check!(part3 <-             62485 ; &input.load(3));
}

fn part1(input: &str) -> String {
    cycle(input.parse().unwrap(), 3, DIVISOR1)
        .1
        .unwrap()
        .to_string()
    // (x, y) = (x0 + (x ** 2 - y ** 2) / 10, y0 + (2 * x * y) / 10);
}

impl std::fmt::Display for Complex {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{},{}]", self.real, self.imag)
    }
}

fn part2(input: &str) -> usize {
    frac_engrave(input.parse().unwrap(), 10)
}

fn part3(input: &str) -> usize {
    frac_engrave(input.parse().unwrap(), 1)
}

const DIVISOR1: Complex = Complex::n(10, 10);
const DIVISOR2: Complex = Complex::n(100_000, 100_000);

fn cycle(p: Complex, cycles: usize, divisor: Complex) -> (usize, Option<Complex>) {
    let mut r = Complex::n(0i64, 0i64);
    for i in 0..cycles {
        r *= r;
        r /= divisor;
        r += p;

        if r.can_engrave() {
            return (i, None);
        }
    }
    (0, Some(r))
}

#[cfg(not(feature = "visualize"))]
fn frac_engrave(p: Complex, precision: usize) -> usize {
    let cycles = 100;
    let size = 1001i64;
    let mut total = 0;

    for y in (0..size).step_by(precision) {
        'next: for x in (0..size).step_by(precision) {
            let p = Complex::n(p.real + x, p.imag + y);
            if cycle(p, cycles, DIVISOR2).1.is_none() {
                if cfg!(feature = "print") {
                    print!(" ");
                }
                continue 'next;
            }
            if cfg!(feature = "print") {
                print!("▫");
            }
            total += 1;
        }
        if cfg!(feature = "print") {
            println!();
        }
    }
    total
}

#[cfg(feature = "visualize")]
fn frac_engrave(p: Complex, precision: usize) -> usize {
    let cycles = 100;
    let size = 1001i64;
    let mut total = 0;

    let pallete = Palette::ocean();
    let mut imgbuf = image::ImageBuffer::new(size as u32, size as u32);

    for y in (0..size).step_by(precision) {
        'next: for x in (0..size).step_by(precision) {
            let p = Complex::n(p.real + x, p.imag + y);
            let (n, v) = cycle(p, cycles, DIVISOR2);
            if v.is_none() {
                let pixel = imgbuf.get_pixel_mut(x as u32, y as u32);
                let color = pallete.color(n as f32 / 255 as f32);
                *pixel = image::Rgb(color);
                continue 'next;
            }
            total += 1;
        }
    }
    imgbuf.save(format!("fractal{precision}.png")).unwrap();
    total
}

#[derive(Copy, Clone)]
struct Complex {
    real: i64,
    imag: i64,
}

impl Complex {
    const fn n(real: i64, imag: i64) -> Self {
        Self { real, imag }
    }

    const fn can_engrave(&self) -> bool {
        self.real.abs() > 1_000_000 || self.imag.abs() > 1_000_000
    }
}

impl std::str::FromStr for Complex {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let start = s.trim().find('[').unwrap() + 1;
        let s = &s[start..s.len() - 1];
        let (a, b) = s.split_once(',').unwrap();
        Ok(Self::n(a.parse().unwrap(), b.parse().unwrap()))
    }
}

// [X1,Y1] * [X2,Y2] = [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]
impl Mul for Complex {
    type Output = Self;

    fn mul(self, rhs: Self) -> Self::Output {
        Self::n(
            self.real * rhs.real - self.imag * rhs.imag,
            self.real * rhs.imag + self.imag * rhs.real,
        )
    }
}

impl MulAssign for Complex {
    fn mul_assign(&mut self, rhs: Self) {
        *self = *self * rhs;
    }
}

// [X1,Y1] / [X2,Y2] = [X1 / X2, Y1 / Y2]
impl Div for Complex {
    type Output = Self;

    fn div(self, rhs: Self) -> Self::Output {
        Self::n(self.real / rhs.real, self.imag / rhs.imag)
    }
}

impl DivAssign for Complex {
    fn div_assign(&mut self, rhs: Self) {
        *self = *self / rhs;
    }
}

// [X1,Y1] + [X2,Y2] = [X1 + X2, Y1 + Y2]
impl Add for Complex {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self::n(self.real + rhs.real, self.imag + rhs.imag)
    }
}

impl AddAssign for Complex {
    fn add_assign(&mut self, rhs: Self) {
        *self = *self + rhs;
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn part1_example() {
        let input = "A=[25,9]";
        assert_eq!("[357,862]", part1(input));
    }

    #[test]
    fn part2_example() {
        let input = "A=[35300,-64910]";
        assert_eq!(4076, part2(input));
    }

    #[test]
    fn part3_example() {
        let input = "A=[35300,-64910]";
        assert_eq!(406954, part3(input));
    }
}
