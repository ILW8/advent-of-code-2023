from typing import List

from line_profiler_pycharm import profile

from input_reader import read_input_from_file
import numpy as np


def print_tree(tree):
    for idx, row in enumerate(tree):
        row_str_elems = []
        for number in row:
            row_str_elems.append(str(number).center(7))
        print(str(idx).rjust(3, '0'), ":", ' ' * idx * 5, '   '.join(row_str_elems))


@profile
def part1(input_lines: List[str]):
    result = 0
    value_histories = []
    history_trees = []

    for line in input_lines:
        value_histories.append(list(map(int, line.split())))

    for row in value_histories:
        new_rows = [row]
        while True:
            new_row = []
            for idx, val in enumerate(row[1:]):
                new_row.append(val - row[idx])
            new_rows.append(new_row)

            assert len(new_row) > 0
            if sum(map(abs, new_row)) == 0:
                break
            row = new_row
        history_trees.append(new_rows)

    # extrapolate
    for tree in history_trees:
        last_val = 0
        for row in tree[::-1]:
            last_val += row[-1]
        result += last_val

    print(f"part1: {result}")


def part2(input_lines: List[str]):
    result = None
    print(f"part2: {result}")


if __name__ == '__main__':
    use_sample = False
    puzzle_input = read_input_from_file("09_sample.txt" if use_sample else "09.txt")
    part1(puzzle_input)
    part2(puzzle_input)
