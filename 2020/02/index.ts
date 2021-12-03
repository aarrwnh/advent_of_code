import { readLines } from "../utils";


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

		const bits = [password[position1], password[position2]].filter((x) => x === bit);
		if (bits.length === 1) {
			count++;
		}
	}
	return count;
}

async function main(file: string) {
	const lines = await readLines<string>(file);
	const result1 = part1(lines);
	const result2 = part2(lines);
	console.log(file, "\t", [result1, result2]);
}

main("02/example.txt");
// 2
// 1
main("02/puzzle.txt");
// 586
// 352
