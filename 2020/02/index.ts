import { check, readLines } from "../utils.ts";

function part1(lines: string[]) {
	const ret = [];
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i].split(" ");
		const range = line[0].split("-").map((x) => Number(x));
		const bit = line[1].replace(":", "");
		const bits = line[2].split("").filter((x) => {
			return x === bit ? true : false;
		});

		if (bits.length >= range[0] && bits.length <= range[1]) {
			ret.push(true);
		}
	}
	return ret.length;
}

function part2(lines: string[]) {
	let count = 0;
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i].split(":");
		const password = line[1];
		const a = line[0].split(/[-\x20]/);
		const position1 = Number(a[0]);
		const position2 = Number(a[1]);
		const bit = a[2];

		const bits = [password[position1], password[position2]].filter((x) =>
			x === bit
		);
		if (bits.length === 1) {
			count++;
		}
	}
	return count;
}

async function main() {
	const sample = await readLines<string>("../input/2020/02/sample.input");
	const puzzle = await readLines<string>("../input/2020/02/puzzle.input");

	check(2, part1(sample));
	check(586, part1(puzzle));

	check(1, part2(sample));
	check(352, part2(puzzle));
}

main();
