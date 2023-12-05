import fs from "fs";
import path from 'path';

const __dirname = path.resolve(import.meta.url);

async function loadFile(path) {
	return new Promise(resolve => {
		fs.readFile(new URL(path, import.meta.url), "utf8", (err, data) => {
			if (err) {
				console.error(err);
				return;
			}
			resolve(data);
		})
	});
}

async function parseFile(path) {
	return await loadFile(path)
		.then(data =>
			data
				.split("\n")
				.map(line => line.split("\x20"))
		);
}

async function parse(path, part2 = false) {
	let position = 0;
	let depth = 0;
	let aim = 0;

	const input = await parseFile(path);
	input.forEach(coord => {
		coord[1] = Number(coord[1])
		const [direction, units] = coord;

		switch (direction) {
			case "down":
				// aim += units; // correct way for part2
				depth += units;
				break;
			case "up":
				// aim -= units; // part2
				depth -= units;
				break;
			case "forward":
				position += units;
				if (part2) {
					// depth += (aim * units); // part2
					aim += (depth * units);
				}
				break;
		}
	});
	if (part2) {
		// flip things..
		return [position, aim, aim * position];
	}
	return [depth, position, depth * position];
}

async function main() {
	console.log(await parse("sample.input"), 150);
	console.log(await parse("puzzle.input"), 1727835);

	console.log(await parse("sample.input", true), 900);
	console.log(await parse("puzzle.input", true), 1544000595);
}

main()
