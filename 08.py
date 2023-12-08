from typing import List
import tqdm
from line_profiler_pycharm import profile

from input_reader import read_input_from_file


def part1(input_lines: List[str]):
    left_right, node_map = parse_input(input_lines)
    print(left_right)
    print(node_map)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        for direction in left_right:
            current_node = node_map[current_node][0 if direction == "L" else 1]
            steps += 1
    print(f"part 1: done in {steps} steps")


def main(input_lines: List[str]):
    left_right, node_map = parse_input(input_lines)

    # part 2
    loop_map = dict()
    nodes = [node for node in node_map.keys() if node.endswith("A")]
    pbar = tqdm.tqdm()

    def advance_single_node(node: str) -> str:
        start_node = node
        for d in left_right:
            node = node_map[node][d == "R"]
        loop_map[start_node] = node
        return node

    lr_length = len(left_right)
    big_step = 0
    while True:
        nodes = [loop_map[node] if node in loop_map else advance_single_node(node) for node in nodes]
        pbar.update(lr_length)

        do_break = True
        for node in nodes:
            if not node.endswith("Z"):
                do_break = False
                break
        if do_break:
            break
        big_step += 1
    print(f"done in {big_step * lr_length} steps")


def parse_input(input_lines):
    left_right = input_lines[0]
    node_map = {node: (left, right) for node, left, right in [(row.split("=")[0].strip(),
                                                               *row.replace("(", "")
                                                               .replace(")", "")
                                                               .replace(" ", "")
                                                               .split("=")[1].split(",")) for row in input_lines[2:]]}
    return left_right, node_map


if __name__ == '__main__':
    puzzle_input = read_input_from_file("08.txt")
    part1(puzzle_input)
    main(puzzle_input)
