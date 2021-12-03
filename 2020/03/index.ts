import { readLines } from "../utils";

const tree = "#";

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
		if (nextRow[position] === tree) {
			countTrees++;
			nextRow[position] = "X";
		}
		else {
			nextRow[position] = "O";
		}
		if (nextPosition > lineMaxIndex) {
			position = nextPosition - lineMaxIndex - 1;
		}
		else {
			position += slope[0];
		}
	}
	return countTrees;
}

async function parse(file: string) {
	const lines = await readLines<string>(file);
	const results = [];
	for (const slope of [
		[1, 1],
		[3, 1],
		[5, 1],
		[7, 1],
		[1, 2]
	]) {
		results.push(countTrees(lines, slope));
	}

	console.log(file, "\t", results[1], results.reduce((acc, curr) => acc * curr, 1), results);
}

async function main() {
	await parse("03/puzzle.txt");
	// 216
	//  [ 79, 216, 91, 96, 45 ] => 6708199680

	await parse("03/example.txt");
	// part1: 7
	// part2: [ 2, 7, 3, 4, 2 ] => 336
}

main();
