export async function readLines<T extends number | string>(file: string): Promise<T[]> {
	const text = await Deno.readTextFile(file);

	const lines = text.split("\n").map((x) =>
		Number.isNaN(Number(x)) ? x.trim() : Number(x)
	);

	return lines as T[];
}
