const example = [
	35,
	20,
	15,
	25,
	47,
	40,
	62,
	55,
	65,
	95,
	102,
	117,
	150,
	182,
	127,
	219,
	299,
	277,
	309,
	576,
];

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

function check(expected: number, result: number): void {
	console.log(expected == result, expected, result);
}

async function main() {
	const __dirname = new URL(".", import.meta.url).pathname;
	const puzzle = await Deno.readTextFile(
		__dirname.slice(__dirname.startsWith("/") ? 1 : 0) + "puzzle.txt",
	).then((
		data,
	) => data.trim().split("\n").map((x) => Number(x)));

	// part1
	check(127, part1(example, 5));
	check(3199139634, part1(puzzle, 25));

	// part2
	check(62, part2(example, 127));
	check(438559930, part2(puzzle, 3199139634));
}

main();
