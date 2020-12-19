import fs from "fs";

export async function readLines<T extends number | string>(file: string): Promise<T[]> {
	return new Promise((resolve) => {
		fs.readFile(file, "utf8", (err, data) => {
			if (err) return err;

			const lines = data.split("\n").map((x) => Number.isNaN(Number(x)) ? x.trim() : Number(x));

			resolve(lines as T[]);
		});
	});
}