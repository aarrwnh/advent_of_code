from typing import List, NewType, Union
import os

Board = NewType("Board", List[List[str]])
BoardGrid = NewType("BoardGrid", List[List[int]])


def read_file(filename: str):
    drawn: List[str] = []
    boards: List[Board] = []
    path = os.path.dirname(__file__) + "/" + filename
    with open(path, "r") as f:
        for x, line in enumerate(f.readlines()):
            if x == 0:
                drawn = line.rstrip().split(",")
                continue

            if line == "\n":
                boards.append([])
                continue

            numbers = list(filter(lambda x: x != "", line.rstrip().split("\x20")))
            boards[len(boards) - 1].append(numbers)

    return (drawn, boards)


def bingo_check(grid: BoardGrid, board: Board) -> Union[List[str], None]:
    grid_size = len(grid)
    for x, row in enumerate(grid):
        if sum(row) == grid_size:
            return board[x]
        column = [r[x] for r in grid]
        if sum(column) == grid_size:
            return [r[x] for r in board]
    return None


def get_unmarked_numbers(grid: BoardGrid, board: Board) -> List[str]:
    grid_size = len(grid)
    unmarked: List[str] = []
    for x, row in enumerate(grid):
        for y in range(0, grid_size):
            if row[y] == 0:
                unmarked.append(board[x][y])
    return unmarked


def sum_str(row: List[str]) -> int:
    return sum(map(lambda x: int(x), row))


def bingo_game(numbers: List[str], boards: List[Board], first_won: bool = True):
    participants = len(boards)  # no. of boards
    grid_size = len(boards[0][0])
    won_boards: List[int] = []
    matrix = [
        [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        for _ in range(participants)
    ]

    #  numbers = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13".split(",")
    unmarked: List[str] = []

    for number in numbers:
        for i, board in enumerate(boards):
            for j, row in enumerate(board):
                if number in row:
                    matrix[i][j][row.index(number)] = 1
                    bingo = bingo_check(matrix[i], board)
                    if bingo:
                        if i not in won_boards:
                            won_boards.append(i)
                        unmarked = get_unmarked_numbers(matrix[i], board)
                        matrix[i][j][row.index(number)] = 2
                        if first_won:
                            return (number, unmarked)
                if len(won_boards) == participants:
                    return (number, unmarked)
    raise AssertionError("no winners")


def part1(numbers: List[str], boards: List[Board]):
    bingo = bingo_game(numbers, boards)
    return sum_str(bingo[1]) * int(bingo[0])


def part2(numbers: List[str], boards: List[Board]):
    bingo = bingo_game(numbers, boards, False)
    return sum_str(bingo[1]) * int(bingo[0])


def main() -> None:
    sample = read_file("sample.input")
    puzzle = read_file("puzzle.input")

    #  pprint(sample)

    print(part1(sample[0], sample[1]), 4512)
    print(part1(puzzle[0], puzzle[1]), 49686)

    print(part2(sample[0], sample[1]), 1924)
    print(part2(puzzle[0], puzzle[1]), 26878)


if __name__ == "__main__":
    main()
