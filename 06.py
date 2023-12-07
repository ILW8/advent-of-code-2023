from typing import List
from input_reader import read_input_from_file


def prod_races(races: list):
    solutions_product = 1
    for time, distance in races:
        race_solutions = 0
        # going to use a naive approach instead of using sympy
        for time_held in range(time + 1):
            total_distance = (time - time_held) * time_held
            if total_distance > distance:
                race_solutions += 1

        solutions_product *= race_solutions
    return solutions_product


def main(input_lines: List[str]):
    # list of (time, distance)-tuples
    races = zip(map(int, input_lines[0].split()[1:]), map(int, input_lines[1].split()[1:]))

    print(prod_races(races))


def part2(input_lines: List[str]):
    time = int(''.join(input_lines[0].split()[1:]))
    distance = int(''.join(input_lines[1].split()[1:]))
    print(prod_races([(time, distance)]))


if __name__ == '__main__':
    main(read_input_from_file("06.txt"))
    part2(read_input_from_file("06.txt"))
