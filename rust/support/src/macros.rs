// use std::time::SystemTime;

// pub fn timing<F: Fn() -> T, T>(f: F) -> T {
//     let start = SystemTime::now();
//     let result = f();
//     let end = SystemTime::now();
//     let duration = end.duration_since(start).unwrap();
//     println!("> {} µs", duration.as_micros());
//     result
// }

pub fn truncate_and_mark_micro(time: u128, n: usize) -> String {
    let mut time = time.to_string();
    if let Some(r) = n.checked_sub(time.len()) {
        time.insert_str(0, &"0".repeat(r));
    }

    time[time.len() - n..time.len()]
        .chars()
        .collect::<Vec<_>>()
        .chunks(3)
        .enumerate()
        .map(|(i, s)| {
            let s = String::from_iter(s.iter());
            if i == 1 {
                format!("\x1b[38;5;249m{}\x1b[0m", s)
            } else {
                s
            }
        })
        .collect()
}

#[macro_export]
macro_rules! check {

    ($name:tt $fn:ident $([ $expect:literal $($input:tt)* ])* ) => {{
        // $( $hide_print:tt)?
        // let mut hide_print = false;
        // $ ( hide_print = $hide_print; )?;
        println!(" \x1b[38;5;240m{name}\x1b[0m", name = $name);
        $(
            let now = std::time::Instant::now();
            // TODO: unpack multiple arguments, atm using one struct instead
            // let out = $fn(($($input),+));
            let out = $fn($($input)?);
            let mut color = "31";
            if $expect == out {
                color = "32";
            }
            let time = now.elapsed().as_micros();
            let seconds = (time / 1000000).to_string();
            println!(" {:>5}.{}s {text}   {mi}ms",
                if seconds == "0" { " " } else { &seconds },
                $crate::truncate_and_mark_micro(time % 1000000000, 6),
                mi = now.elapsed().as_millis(),
                text = format!(" \x1b[{color}m {out:>10?} \x1b[0m")
            );
            assert_eq!($expect, out);
        )*
        println!();
    }};
}

#[deprecated(note = "use check!(fn [value stuct]*) macro")]
#[macro_export]
macro_rules! check_values {
    (
        $expect:expr,
        $fn:expr,
        $file:expr
        $(, $hide_print:expr)?
    ) => {{
        let mut hide_print = false;
        $ ( hide_print = $hide_print; )?;

        let start = std::time::SystemTime::now();
        let out = $fn($file);
        let end = std::time::SystemTime::now();
        let duration = end.duration_since(start).unwrap();
        println!("> {} µs", duration.as_micros());
        let mut color = "41";
        if $expect == out {
            color = "42";
        }

        if !hide_print {
            println!("  \x1b[{}m\x1b[30m {:?} == {:?} \x1b[00m", color, $expect, out);
        }
        assert_eq!($expect, out);
    }};
}

#[deprecated(note = "WIUP")]
#[macro_export]
macro_rules! asserter1 {
    (
        $expect:tt,
        [$($input:tt)*]
    // $($hide_print:expr)?, $(,)+,
    ) => {
        // let mut hide_print = false;
        // $ ( hide_print = $hide_print; )?;

        let start = std::time::SystemTime::now();
        let out = $fn($($input)*);
        // let end = std::time::SystemTime::now();
        // let duration = end.duration_since(start).unwrap();
        // println!("> {} µs", duration.as_micros());
        // let mut color = "41";
        // if $expect == out {
        //     color = "42";
        // }

        // if !hide_print {
            // println!("  \x1b[{}m\x1b[30m {:?} == {:?} \x1b[00m", color, $expect, out);
        // }
        // assert_eq!($expect, $output);
    };

    // (
    //     $expect:expr,
    //     $fn:expr,
    //     $($input:tt)+,*
    //     $(, $hide_print:expr)?
    // ) => {
    //     let mut hide_print = false;
    //     $ ( hide_print = $hide_print; )?;
    //     println!("we are here");
    // }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn prefix_three_no_color() {
        assert_eq!("001", &truncate_and_mark_micro(1234, 6)[0..3]);
        assert_eq!("000", &truncate_and_mark_micro(123, 6)[0..3]);
    }
}
