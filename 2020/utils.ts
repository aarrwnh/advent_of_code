export async function readLines<T extends number | string>(file: string): Promise<T[]> {
	if (!file) {
		throw new Error("no file");
	}
	const __dirname = new URL(".", import.meta.url).pathname;
	const text = (await Deno.readTextFile(
		__dirname.slice(__dirname.startsWith("/") ? 1 : 0) + file,
	)).trim();

	const lines = text.split("\n").map((x) =>
		Number.isNaN(Number(x)) ? x.trim() : Number(x)
	);

	return lines as T[];
}

function red(s: string) {
	console.log(`\x1b[41m\x1b[30m${s}\x1b[0m`);
}

function green(s: string) {
	console.log(`\x1b[42m\x1b[30m${s}\x1b[0m`);
}

export function check(expected: unknown, result: unknown): void {
	const check = expected === result;
	const out = `${expected} == ${result}`;
	if (check) {
		green(out);
	} else {
		red(out);
	}
}
