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
		# mkdir -p "../input/$1/${day}"
		touch "../input/$1/${day}-example"
		touch "../input/$1/${day}-puzzle"
		cp "../templates__/python" "$1/day${day}.py"
		sed -i -e "s/%year%/$1/" -e "s/%day%/$2/" "$1/day${day}.py"
	fi
else
	echo "no command"
fi
