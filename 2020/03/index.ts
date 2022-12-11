import { check, readLines } from "../utils.ts";

const TREE = "#";

function countTrees(lines: string[], slope: number[]) {
	let countTrees = 0;
	let position = slope[0];
	const lineMaxIndex = lines[0].length - 1;
	for (let i = 0; i < lines.length - 1; i += slope[1]) {
		if (!lines[i + slope[1]]) {
			break;
		}
		const nextPosition = position + slope[0];
		const nextRow = lines[i + slope[1]].split("");
		if (nextRow[position] === TREE) {
			countTrees++;
			nextRow[position] = "X";
		} else {
			nextRow[position] = "O";
		}
		if (nextPosition > lineMaxIndex) {
			position = nextPosition - lineMaxIndex - 1;
		} else {
			position += slope[0];
		}
	}
	return countTrees;
}

const SLOPES = [
	[1, 1],
	[3, 1],
	[5, 1],
	[7, 1],
	[1, 2],
];

function part1(lines: string[]) {
	const results = [];
	for (const slope of SLOPES) {
		results.push(countTrees(lines, slope));
	}

	return results[1];
}

function part2(lines: string[]) {
	const results = [];
	for (const slope of SLOPES) {
		results.push(countTrees(lines, slope));
	}

	return results.reduce((acc, curr) => acc * curr, 1);
}

async function main() {
	const sample = await readLines<string>("../input/2020/03/sample.input");
	const puzzle = await readLines<string>("../input/2020/03/puzzle.input");

	check(7, part1(sample));
	check(216, part1(puzzle));

	check(336, part2(sample));
	check(6708199680, part2(puzzle));
}

main();
