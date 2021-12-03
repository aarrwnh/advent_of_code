import fs from "fs";
import { readLines } from "../utils";

const cache: number[] = [];
function part1(lines: number[], result: number) {
	for (let i = 0; i < lines.length; i++) {
		const item = result - lines[i];
		cache.push(lines[i]);
		const idx = cache.indexOf(item);
		if (idx !== -1) {
			return lines[i] * cache[idx];
		}
	}
	return -1;
}

function part2(lines: number[], result: number) {
	for (let i = 0; i < lines.length; i++) {
		for (let j = 0; j < lines.length; j++) {
			for (let d = 0; d < lines.length; d++) {
				if (lines[d] + lines[j] + lines[i] === result) {
					return lines[d] * lines[j] * lines[i];
				}
			}
		}
	}
	return -1;
}

async function main(file: string, result: number) {

	const lines = await readLines<number>(file);

	const result1 = part1(lines, result);
	const result2 = part2(lines, result);

	console.log(file, "\t", [result1, result2]);
}

main("01/example.txt", 2020);
// 514579
// 241861950

main("01/puzzle.txt", 2020);
// 788739
// 178724430
