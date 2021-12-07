const example = [
	"light red bags contain 1 bright white bag, 2 muted yellow bags.",
	"dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
	"bright white bags contain 1 shiny gold bag.",
	"muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
	"shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
	"dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
	"vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
	"faded blue bags contain no other bags.",
	"dotted black bags contain no other bags.",
];

const part2Example2 = [
	"shiny gold bags contain 2 dark red bags.",
	"dark red bags contain 2 dark orange bags.",
	"dark orange bags contain 2 dark yellow bags.",
	"dark yellow bags contain 2 dark green bags.",
	"dark green bags contain 2 dark blue bags.",
	"dark blue bags contain 2 dark viole bags.",
	"dark violet bags contain no other bags.",
];

interface BagContents {
	color: string;
	amount: number;
}

function parseRawInput(input: string[]): [string, BagContents[]][] {
	const parsed: [string, BagContents[]][] = [];
	for (const line of input) {
		const [parentBag, childBags] = line.replace(/ bags?/g, "").slice(0, -1)
			.split("contain");
		if (!childBags.includes("no other")) {
			const bags: BagContents[] = childBags
				.split(", ")
				.map((x) => {
					const b = x.match(/([0-9]+)(.+)/);
					if (b === null) throw new Error("can't be null");
					return {
						color: b[2].trim(),
						amount: Number(b[1]),
					};
				});
			parsed.push([parentBag.trim(), bags]);
		}
	}
	return parsed;
}

function filterPuzzle(inputData: string[]) {
	const input = parseRawInput(inputData);
	const parents: Record<string, string[]> = {};
	const children: Record<string, BagContents[]> = {};

	for (const line of input) {
		const [parentBag, childBags] = line;
		if (!children[parentBag]) {
			children[parentBag] = [];
		}
		childBags.forEach((bag) => {
			children[parentBag].push(bag);
			if (bag.color !== "empty") {
				if (!parents[bag.color]) {
					parents[bag.color] = [];
				}
				if (!(parentBag in parents[bag.color])) {
					parents[bag.color].push(parentBag);
				}
			}
		});
	}
	return { parents, children };
}

function collectParentColors(arr: Record<string, string[]>, color: string): string[] {
	const ret = [color];
	if (arr[color]) {
		for (const parent of arr[color]) {
			ret.push(...collectParentColors(arr, parent));
		}
	}
	return ret;
}

function countChildBags(
	arr: Record<string, BagContents[]>,
	count: number,
	colorName: string,
) {
	const n = count;
	if (arr[colorName]) {
		for (const { amount, color } of arr[colorName]) {
			count += countChildBags(arr, n * amount, color);
		}
	}
	return count;
}

function parse(inputData: string[], part2 = false): number {
	const { parents, children } = filterPuzzle(inputData);
	const parentBags = new Set(collectParentColors(parents, "shiny gold"));
	if (part2) {
		const bagCount = (countChildBags(children, 1, "shiny gold"));
		return bagCount - 1;
	} else {
		return parentBags.size - 1;
	}
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
	) => data.trim().split("\n"));

	// part1
	check(4, parse(example));
	check(268, parse(puzzle));

	// part2
	check(32, parse(example, true));
	check(126, parse(part2Example2, true));
	check(7867, parse(puzzle, true));
}

main();

// Redir !set NO_COLOR=true && deno run --allow-all 2020\07\index.ts
// !deno fmt --config .\deno.json 07\index.ts
