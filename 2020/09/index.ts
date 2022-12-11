import { check, readLines } from "../utils.ts";

function part1(inputData: number[], preamble = 5): number {
	const invalid: number[] = [];
	for (let idx = preamble; idx < inputData.length; idx++) {
		const n = inputData[idx];

		const prevNumbers = inputData.slice(idx - preamble, idx);
		let isValid = false;
		for (let j = 0; j < preamble; j++) {
			const firstNumber = prevNumbers[j];
			for (let i = 0; i < prevNumbers.length; i++) {
				const secondNumber = prevNumbers[i];
				if (firstNumber === secondNumber) {
					continue;
				}
				if (firstNumber + secondNumber === n) {
					isValid = true;
					break;
				}
			}
			if (isValid) {
				break;
			}
		}

		if (!isValid) {
			invalid.push(n);
		}
	}

	return invalid[0];
}

function part2(inputData: number[], invalidNumber: number): number {
	const startIdx = inputData.indexOf(invalidNumber);
	const n = inputData[startIdx];
	const currentNumbers: number[] = [];
	for (let i = startIdx - 1; i > 0; i--) {
		currentNumbers.push(inputData[i]);
		const sum = currentNumbers.reduce((a, v) => a + v, 0);
		if (sum > n) {
			currentNumbers.shift();
		}
		if (sum === n) {
			break;
		}
	}

	currentNumbers.sort();
	return currentNumbers[0] + currentNumbers[currentNumbers.length - 1];
}

async function main() {
	const sample = await readLines<number>("../input/2020/09/sample.input");
	const puzzle = await readLines<number>("../input/2020/09/puzzle.input");

	check(127, part1(sample, 5));
	check(3199139634, part1(puzzle, 25));

	check(62, part2(sample, 127));
	check(438559930, part2(puzzle, 3199139634));
}

main();
