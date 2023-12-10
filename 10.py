from typing import List

from line_profiler_pycharm import profile

from input_reader import read_input_from_file

import numpy as np


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = {
    'UP': np.array(UP),
    'DOWN': np.array(DOWN),
    'LEFT': np.array(LEFT),
    'RIGHT': np.array(RIGHT)
}
#
DIRECTIONS = {
    'UP': UP,
    'DOWN': DOWN,
    'LEFT': LEFT,
    'RIGHT': RIGHT
}


PIPE_TYPES = {
    '|': [(0, 1), (0, -1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, 1), (1, 0)],
    'J': [(-1, 0), (0, 1)],
    '7': [(-1, 0), (0, -1)],
    'F': [(0, -1), (1, 0)],
    '.': None
}


@profile
def traverse_pipes(position, connectivity_map, distance_map):
    distance_map[position[1]][position[0]] = 0
    visited = {position}
    queue = [position]

    while queue:
        current = queue.pop(0)
        current_x, current_y = current
        current_distance = distance_map[current_y][current_x]

        for direction in [UP, DOWN, LEFT, RIGHT]:
            new_x, new_y = current[0] + direction[0], current[1] + direction[1]
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


@profile
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

    # distance_map[start_position[1]][start_position[0]] = 0

    traverse_pipes(start_position, connectivity_map, distance_map)

    print(np.max(np.array(distance_map)))


def part2(input_lines: List[str]):
    pass


if __name__ == '__main__':
    use_sample = False
    puzzle_input = read_input_from_file("10_sample.txt" if use_sample else "10.txt")
    part1(puzzle_input)
    part2(puzzle_input)
