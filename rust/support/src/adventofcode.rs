#[macro_export]
macro_rules! check_values {
    ($expect:expr, $output:expr) => {{
        let mut color = "41";
        if $expect == $output {
            color = "42";
        }
        println!(
            "\x1b[{}m\x1b[30m{:?} == {:?}\x1b[00m",
            color, $expect, $output
        );
        // assert_eq!($expect, $output);
    }};
}
