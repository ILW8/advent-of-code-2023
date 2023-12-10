import functools
from typing import List
from input_reader import read_input_from_file
import numpy as np
from termcolor import colored
from matplotlib import pyplot as plt

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

PIPE_TYPES = {
    '|': [(0, 1), (0, -1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, 1), (1, 0)],
    'J': [(-1, 0), (0, 1)],
    '7': [(-1, 0), (0, -1)],
    'F': [(0, -1), (1, 0)],
    '.': None
}
PIPE_NP_TYPES = {
    '|': np.array([[0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]]),
    '-': np.array([[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]]),
    'L': np.array([[0, 1, 0],
                   [0, 1, 1],
                   [0, 0, 0]]),
    'J': np.array([[0, 1, 0],
                   [1, 1, 0],
                   [0, 0, 0]]),
    '7': np.array([[0, 0, 0],
                   [1, 1, 0],
                   [0, 1, 0]]),
    'F': np.array([[0, 0, 0],
                   [0, 1, 1],
                   [0, 1, 0]]),
    'S': np.array([[0, 2, 0],
                   [2, 2, 2],
                   [0, 2, 0]]),
    '.': np.array([[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]),
}


def traverse_pipes(position, connectivity_map, distance_map):
    distance_map[position[1]][position[0]] = 0
    visited = {position}
    queue = [position]

    while queue:
        current = queue.pop(0)
        current_x, current_y = current
        current_distance = distance_map[current_y][current_x]

        for direction in [UP, DOWN, LEFT, RIGHT]:
            current_connectivity = connectivity_map[current_y][current_x]
            should_skip = True

            for connectivity in current_connectivity:
                if (connectivity[0] == direction[0]) and (connectivity[1] == -direction[1]):
                    should_skip = False
                    break

            if should_skip:
                continue

            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            if new_x < 0 or new_y < 0:
                continue

            neighbour = (new_x, new_y)
            if neighbour in visited:
                continue

            try:
                new_connectivity = connectivity_map[new_y][new_x]
                if not new_connectivity:
                    continue
            except IndexError:
                continue

            should_skip = True
            for connectivity in new_connectivity:
                if (connectivity[0] == -direction[0]) and (connectivity[1] == direction[1]):
                    should_skip = False
                    break

            if should_skip:
                continue

            visited.add(neighbour)
            queue.append(neighbour)
            distance_map[new_y][new_x] = current_distance + 1
    print()


def part1(input_lines: List[str]):
    start_position = None
    connectivity_map = [[[]] * len(input_lines[0]) for _ in range(len(input_lines))]
    distance_map = [[-1] * len(input_lines[0]) for _ in range(len(input_lines))]
    for row_index, line in enumerate(input_lines):
        for column_index, character in enumerate(line):
            if character == "S":
                start_position = (column_index, row_index)
                continue
            connected_sides = PIPE_TYPES[character]
            if connected_sides is None:
                continue

            connectivity_map[row_index][column_index] = connected_sides
    connectivity_map[start_position[1]][start_position[0]] = [UP, DOWN, LEFT, RIGHT]
    traverse_pipes(start_position, connectivity_map, distance_map)
    print(np.max(np.array(distance_map)))
    return np.array(distance_map)


def pretty_print_pipes(input_lines: List[str], use_colors=False):
    for idx, line in enumerate(input_lines):
        line = line.replace("7", "┓")
        line = line.replace("L", "┗")
        line = line.replace("J", "┛")
        line = line.replace("F", "┏")
        line = line.replace("-", "━")
        line = line.replace("|", "┃")
        line = line.replace(".", " ")

        if use_colors:
            grey = idx % 2 == 1
            for character in line:
                if grey:
                    print(colored(character, "white", "on_dark_grey", force_color=True), end="")
                else:
                    print(colored(character, "white", "on_black", force_color=True), end="")
                grey = not grey
            continue

        print(line)


def filter_main_loop(input_lines: List[str], distance_map: np.array):
    main_loop_bitmap = distance_map >= 0
    filtered_input = []
    for row, line in enumerate(input_lines):
        a = np.array(list(line))
        a[~main_loop_bitmap[row]] = '.'
        filtered_input.append(''.join(a))
    return filtered_input


def part2(input_lines: List[str]):
    bigger_map = np.zeros((len(input_lines[0]) * 3, len(input_lines) * 3))

    for row_index, row in enumerate(input_lines):
        for col_index, col in enumerate(row):
            bigger_map[row_index * 3:row_index * 3 + 3, col_index * 3:col_index * 3 + 3] = PIPE_NP_TYPES[col]

    # BFS tiles outside
    visited = {(0, 0)}
    queue = [(0, 0)]
    while queue:
        current = queue.pop(0)

        for direction in [UP, DOWN, LEFT, RIGHT]:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
            neighbour = (new_x, new_y)

            if (new_x < 0
                    or new_y < 0
                    or new_x >= bigger_map.shape[1]
                    or new_y >= bigger_map.shape[0]
                    or neighbour in visited
                    or bigger_map[new_y][new_x] != 0):
                continue

            visited.add(neighbour)
            queue.append(neighbour)
            bigger_map[new_y][new_x] = 5
    bigger_map[bigger_map == 0] = -5
    # plt.imshow(bigger_map, interpolation='nearest')
    # plt.show()

    inner_count = 0
    for row_index, row in enumerate(input_lines):
        for col_index, col in enumerate(row):
            inner_count += bigger_map[1 + row_index * 3, 1 + col_index * 3] == -5
    print(inner_count)


if __name__ == '__main__':
    use_sample = False
    puzzle_input = read_input_from_file("10_sample.txt" if use_sample else "10.txt")

    # part 1
    loop_distance_map = part1(puzzle_input)

    # part 2
    filtered_main_loop = filter_main_loop(puzzle_input, loop_distance_map)
    pretty_print_pipes(filtered_main_loop)
    part2(filtered_main_loop)

