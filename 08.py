from typing import List
from input_reader import read_input_from_file


def main(input_lines: List[str]):
    left_right = input_lines[0]

    node_map = {node: (left, right) for node, left, right in [(row.split("=")[0].strip(),
                                                               *row.replace("(", "")
                                                               .replace(")", "")
                                                               .replace(" ", "")
                                                               .split("=")[1].split(",")) for row in input_lines[2:]]}
    print(node_map)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        for direction in left_right:
            current_node = node_map[current_node][0 if direction == "L" else 1]
            steps += 1
    print(f"done in {steps} steps")


if __name__ == '__main__':
    main(read_input_from_file("08.txt"))
