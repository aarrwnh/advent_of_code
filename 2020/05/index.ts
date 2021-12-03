import { readLines } from "../utils";

function sortArr(arr: number[]): number[] {
	return arr.sort((a, b) => a > b ? -1 : a < b ? 1 : 0);
}

function reduce(arr: number[], max: number) {
	const range = Array(max + 1).fill(1).map((x, i) => i);
	const n = arr.reduce((range, curr) => {
		const half = Math.round((range.length - 1) / 2);
		if (curr === -1) {
			range.splice(half, range.length - 1);
		}
		else if (curr === 1) {
			range.splice(0, half);
		}
		return range;
	}, range);

	return n.length > 0 ? n[0] : 0;
}

function findEmptyFirstSeatInRange(
	seats: number[],
	columns: number[],
	rows: number[]
): number | void {
	for (let column = columns[0]; column < columns[1]; column++) {
		for (let row = rows[0]; row < rows[1]; row++) {
			const seat = row * 8 + column;
			if (!seats.includes(seat)) {
				return seat;
			}
		}
	}
}

// FBLR 0101
const flags: Record<string, number> = { "F": -1, "B": 1, "L": -1, "R": 1 };

function parseGroups(groups: string[]) {
	const seats: number[] = [];

	for (let i = 0; i < groups.length; i++) {
		const group = groups[i].split("");
		const output = [];

		for (let i = 0; i < group.length; i++) {
			output.push(flags[group[i]]);
		}

		const row = reduce(output.slice(0, 7), 127);
		const column = reduce(output.slice(7), 7);
		const seat = row * 8 + column;

		seats.push(seat);
		// if (row >= maxRows) {
		// 	maxRows = row;
		// }
	}
	console.log("max:", sortArr(seats)[0]);

	console.log("seat:", findEmptyFirstSeatInRange(seats, [0, 7], [14, 102]));
}

async function parse(file: string) {
	const lines = await readLines<string>(file);
	parseGroups(lines);
}

async function main() {
	await parse("05/puzzle.txt");
	// part1: 871
	// part2: 640

	// parseGroups([
	// 	"FBFBBFFRLR",
	// 	"BFFFBBFRRR",
	// 	"FFFBBBFRRR",
	// 	"BBFFBBFRLL"
	// ]);
	// FBFBBFFRLR row: 44 column: 5 seat: 357
	// BFFFBBFRRR row: 70 column: 7 seat: 567
	// FFFBBBFRRR row: 14 column: 7 seat: 119
	// BBFFBBFRLL row: 102 column: 4 seat: 820
}

main();