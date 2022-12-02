use std::time::SystemTime;

pub fn timing<F: Fn() -> T, T>(f: F) -> T {
    let start = SystemTime::now();
    let result = f();
    let end = SystemTime::now();
    let duration = end.duration_since(start).unwrap();
    println!("> {} µs", duration.as_micros());
    result
}

#[macro_export]
macro_rules! check_values {
    ($expect:expr, $fn:expr, $file:expr) => {
        let start = SystemTime::now();
        let out = $fn($file);
        let end = SystemTime::now();
        let duration = end.duration_since(start).unwrap();
        println!("> {} µs", duration.as_micros());
        let mut color = "41";
        if $expect == out {
            color = "42";
        }
        println!("\x1b[{}m\x1b[30m{:?} == {:?}\x1b[00m", color, $expect, out);
        // assert_eq!($expect, $output);
    };
}
