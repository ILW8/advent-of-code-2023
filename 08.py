from functools import reduce
from typing import List
from line_profiler_pycharm import profile

from input_reader import read_input_from_file


def part1(input_lines: List[str]):
    left_right, node_map = parse_input(input_lines)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        for direction in left_right:
            current_node = node_map[current_node][0 if direction == "L" else 1]
            steps += 1
    print(f"part 1: done in {steps} steps")


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)


def lcm_many(*numbers):
    return reduce(lcm, numbers)


@profile
def part2(input_lines: List[str]):
    left_right, node_map = parse_input(input_lines)

    nodes = [node for node in node_map.keys() if node.endswith("A")]
    simultaneous_big_steps = []
    for node in nodes:
        current_node = node
        steps = 0
        big_steps = 0
        while not current_node.endswith("Z"):
            for direction in left_right:
                current_node = node_map[current_node][0 if direction == "L" else 1]
                steps += 1
                if current_node.endswith("A"):
                    print(f"after {steps} steps, node {node} arrived at {current_node}")
            big_steps += 1
        # print(f"{node}: done in {steps} steps ({big_steps} big steps) | "
        #       f"{big_steps}*{len(left_right)} = {big_steps * len(left_right)}")
        simultaneous_big_steps.append(big_steps)

    print(f"part 2: done in {lcm_many(*simultaneous_big_steps) * len(left_right)} steps")


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
    part2(puzzle_input)
