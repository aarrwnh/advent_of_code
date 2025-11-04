use std::sync::LazyLock;

mod permutations;
pub use permutations::Permutations;

static CURRENT_DIR: LazyLock<std::path::PathBuf> = LazyLock::new(|| {
    let mut cwd = std::env::current_dir().unwrap();
    let cwd0 = cwd.clone();
    for _ in 0..3 {
        if cwd.join(".root").is_file() {
            return cwd;
        }
        cwd.pop();
    }
    cwd0
});

fn load_file(p: impl AsRef<std::path::Path>) -> String {
    let p = p.as_ref();
    std::fs::read_to_string(p).expect("file not found")
}

// everybody_codes_e2024_q05_p1.txt
#[derive(Clone, Copy)]
pub struct InputReader {
    event: &'static str,
    quest: u8,
}

impl InputReader {
    #[must_use]
    pub fn new(event: &'static str, quest: u8) -> Self {
        Self { event, quest }
    }

    #[must_use]
    pub fn load(self, part: u8) -> String {
        load_file(CURRENT_DIR.join(format!(
            "quests\\q{q:0>2}\\everybody_codes_{e}_q{q:0>2}_p{part}.txt",
            q = self.quest,
            e = self.event
        )))
    }
}

// pub fn compare<T>(name: &str, a: T, b: T)
// where
//     T: std::fmt::Debug,
//     T: std::fmt::Display,
//     T: PartialEq,
//     T: 'static,
// {
//     if a.eq(&b) {
//         println!("{}: \x1b[42m {} \x1b[0m", name, b);
//     } else {
//         println!("{}: \x1b[41m {} != {} \x1b[0m", name, a, b);
//         // stop execution
//         assert_eq!(a, b);
//     }
// }

#[must_use]
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
            let s = s.iter().collect::<String>();
            if i == 1 {
                format!("\x1b[38;5;249m{s}\x1b[0m")
            } else {
                s
            }
        })
        .collect()
}

#[macro_export]
macro_rules! check {
    ($fn:ident <- $expect:literal ; $($args:expr),+) => {{
        println!(" \x1b[38;5;240m{name}\x1b[0m", name = stringify!($fn));

        let now = std::time::Instant::now();
        let out = $fn( $($args),+ );
        let mut color = if $expect == out { "32" } else { "31" };
        let time = now.elapsed().as_micros();
        let seconds = (time / 1000000);

        println!(" {seconds:>5}.{micro}s {text:>35}  {milis}ms",
            seconds = if seconds == 0 { " " } else { &seconds.to_string() },
            micro = $crate::truncate_and_mark_micro(time % 1000000000, 6),
            milis = now.elapsed().as_millis(),
            text = format!(" \x1b[{color}m {out} \x1b[0m")
        );

        assert_eq!($expect, out);
        println!();
    }};
}
