#!/bin/bash

set -e

if [[ -n "$1" && -n "$2" ]]; then
	day="$2"
	if [[ ${#day} == 1 ]]; then
		day="0$2"
	fi
	if [[ -f "$1/day${day}.py" ]]; then
		echo "file exists"
	else
		mkdir -p "$1"
		mkdir -p "../input/$1/${day}"
		cp "../template__/puzzle" "../input/$1/${day}/"
		cp "../template__/sample" "../input/$1/${day}/"
		cp "../template__/day-python" "$1/day${day}.py"
		sed -i "s/0000\/00/$1\/${day}/" "$1/day${day}.py"
	fi
else
	echo "no command"
fi
