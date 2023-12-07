from typing import List
from input_reader import read_input_from_file


def main(input_lines: List[str]):
    # list of (time, distance)-tuples
    races = zip(map(int, input_lines[0].split()[1:]), map(int, input_lines[1].split()[1:]))

    solutions_product = 1
    for time, distance in races:
        race_solutions = 0
        # going to use a naive approach instead of using sympy
        for time_held in range(time + 1):
            total_distance = (time - time_held) * time_held
            if total_distance > distance:
                race_solutions += 1

        solutions_product *= race_solutions
    print(solutions_product)


if __name__ == '__main__':
    main(read_input_from_file("06.txt"))
