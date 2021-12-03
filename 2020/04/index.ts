import { readLines } from "../utils";

/* 
	 byr (Birth Year) - four digits; at least 1920 and at most 2002.
	 iyr (Issue Year) - four digits; at least 2010 and at most 2020.
	 eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
	 hgt (Height) - a number followed by either cm or in:
		  If cm, the number must be at least 150 and at most 193.
		  If in, the number must be at least 59 and at most 76.
	 hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
	 ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
	 pid (Passport ID) - a nine-digit number, including leading zeroes.
	 cid (Country ID) - ignored, missing or not.

*/
const passportValidationRules: Record<string, any> = {
	"byr": { type: "range", rules: [1920, 2002], range: 2002 - 1920 }, // 1920-2002}=
	"iyr": { type: "range", rules: [2010, 2020], range: 2020 - 2010 },
	"eyr": { type: "range", rules: [2020, 2030], range: 2030 - 2020 },
	"hgt": {
		type: "range",
		rules: { "cm": [150, 193], "in": [59, 76] },
		range: { "cm": 193 - 150, "in": 76 - 59 }
	},
	"hcl": { type: "regex", rules: /^#[0-9a-f]{6}$/ },
	"ecl": { type: "includes", rules: ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"] },
	"pid": { type: "regex", rules: /^[0-9]{9}$/ },
	// "cid" : ""
};

const validPassportKeys = Object.keys(passportValidationRules);

function isRange(min: number, max: number): ((val: number) => boolean) {
	return (value: number) => {
		return min <= value && max >= value;
	};
}

function validateField(field: string, value: string): boolean {
	const rule = passportValidationRules[field];
	switch (rule.type) {
		case "regex": {
			const match = value.match(rule.rules);
			return match !== null;
		}
		case "includes": {
			return rule.rules.includes(value);
		}
		case "range": {
			if (field === "hgt") {
				const height = value.match(/^([0-9]+)([cmin]+)$/);
				if (height !== null) {
					const type = height[2];
					return isRange(rule.rules[type][0], rule.rules[type][1])(Number(height[1]));
				}
			}
			else {
				return isRange(rule.rules[0], rule.rules[1])(Number(value));
			}
		}
	}
	return false;
}

function parseFields(line: Record<string, string | number>, input: string): void {
	const fields = input.split(" ").map((x) => x.split(":"));
	for (const [key, value] of fields) {
		if (
			validPassportKeys.includes(key)
		) {
			const validated = validateField(key, value);
			if (validated) {
				line.validCount = Number(line.validCount) + 1;
			}
			line.count = Number(line.count) + 1;
		}
		line[key] = value;
	}
}

function countValidPassports(passports: Record<string, string | number>[]): number[] {
	let count = 0;
	let validCount = 0;
	for (let i = 0; i < passports.length; i++) {
		if (passports[i].count >= 7) {
			count++;
			if (passports[i].validCount >= 7) {
				validCount++;
			}
		}

	}
	return [count, validCount];
}



async function parse(file: string) {
	const lines = await readLines<string>(file);
	const passports: Record<string, string | number>[] = [];
	passports.push({ count: 0, validCount: 0 });
	let pointer = 0;
	for (let idx = 0; idx < lines.length; idx++) {
		const line = lines[idx];
		if (Number(line) === 0) {
			pointer++;
			passports.push({ count: 0, validCount: 0 });
			continue;
		}
		parseFields(passports[pointer], line);
	}

	console.log(file, "\t", countValidPassports(passports));
}

async function main() {
	await parse("04/puzzle.txt");
	// 170
	// 103

	await parse("04/example.txt");
	// 2
	// 2
}

main();