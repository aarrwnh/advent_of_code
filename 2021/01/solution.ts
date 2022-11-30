let part1 = 0;
let part2 = 0;

const input = await Deno.readTextFile("./01/puzzle.input");

input
	.split("\n")
	.map((i) => Number(i))
	.forEach((val, idx, arr) => {
		if (idx === 0) return;

		if (arr[idx - 1] < val) {
			part1 += 1;
		}

		if (arr[idx] > arr[idx - 3]) {
			part2 += 1;
		}
	});

console.log(part1, part2);
