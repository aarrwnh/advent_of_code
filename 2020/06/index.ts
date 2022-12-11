import { check, readLines } from "../utils.ts";

function getGroups(lines: number[] | string[]) {
	const groups: string[][] = [];
	groups.push([]);
	let pointer = 0;
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		if (line === 0 || line === "") {
			groups.push([]);
			pointer++;
			continue;
		}
		groups[pointer].push(String(line));
	}
	return groups;
}

function filterDuplicates(groups: string[][]) {
	let sum = 0;
	for (let i = 0; i < groups.length; i++) {
		const group = [];
		for (let j = 0; j < groups[i].length; j++) {
			const letter = groups[i][j];
			group.push(...letter.split(""));
		}
		sum += new Set(group).size;
	}
	return sum;
}

function countGroupAnswersPart2_x(groups: string[][]) {
	const count: Record<string, Record<string, number>> = {};
	let sum = 0;

	for (let i = 0; i < groups.length; i++) {
		count[i] = {};
		for (let j = 0; j < groups[i].length; j++) {
			const letter = groups[i][j];

			letter.split("").forEach((x) => {
				if (!count[i][x]) {
					count[i][x] = 0;
				}
				count[i][x] = count[i][x] + 1;
			});
		}

		const x = Object.keys(count[i]);
		const noDupes = new Set(...groups[i]);

		if (groups[i].length === 1) {
			sum += x.length;
		} else if (noDupes.size === x.length) {
			sum += 1;
		} else if (groups[i].length === x.length) {
			sum += 0;
		} else {
			sum += x.length - groups[i].length;
		}
		console.log(groups[i], Object.keys(count[i]));
	}

	return sum;
}

function countGroupAnswersPart2(groups: string[][]) {
	const count: Record<string, (string | number)[]> = {};
	let sum = 0;

	for (let i = 0; i < groups.length; i++) {
		const group = groups[i];

		if (group.length === 1) {
			// count[i] = [group[0].length];
			sum += group[0].length;
		} else {
			for (let j = 0; j < group.length; j++) {
				const letter = group[j];

				letter.split("").forEach((x) => {
					if (!count[i]) {
						count[i] = [];
					}
					count[i].push(x);
				});
			}

			const c = count[i].reduce((acc, curr) => {
				if (!acc[curr]) {
					acc[curr] = 1;
				} else {
					acc[curr] = acc[curr] + 1;
				}
				return acc;
			}, Object.create({}));

			const d = Object.values(c).filter((x) => group.length === x);

			// count[i] = [d.length];
			sum += d.length;
		}
	}

	// 1 person => count all letters => 'abc' => 3

	return sum;
}

function part1(lines: string[]) {
	const groups = getGroups(lines);
	return filterDuplicates(groups);
}

function part2(lines: string[]) {
	const groups = getGroups(lines);
	return countGroupAnswersPart2(groups);
}

async function main() {
	const sample = await readLines<string>("../input/2020/06/sample.input");
	const puzzle = await readLines<string>("../input/2020/06/puzzle.input");

	check(11, part1(sample));
	check(6273, part1(puzzle));

	check(6, part2(sample));
	check(3254, part2(puzzle));
}

main();
