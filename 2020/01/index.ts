import { check, readLines } from "../utils.ts";

const SUM = 2020;

const cache: number[] = [];

function part1(lines: number[]) {
	for (let i = 0; i < lines.length; i++) {
		const item = SUM - lines[i];
		cache.push(lines[i]);
		const idx = cache.indexOf(item);
		if (idx !== -1) {
			return lines[i] * cache[idx];
		}
	}
	return -1;
}

function part2(lines: number[]) {
	for (let i = 0; i < lines.length; i++) {
		for (let j = 0; j < lines.length; j++) {
			for (let d = 0; d < lines.length; d++) {
				if (lines[d] + lines[j] + lines[i] === SUM) {
					return lines[d] * lines[j] * lines[i];
				}
			}
		}
	}
	return -1;
}

async function main() {
	const sample = await readLines<number>("../input/2020/01/sample.input");
	const puzzle = await readLines<number>("../input/2020/01/puzzle.input");

	check(514579, part1(sample));
	check(788739, part1(puzzle));

	check(241861950, part2(sample));
	check(178724430, part2(puzzle));
}

main();
