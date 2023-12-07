from typing import List
from input_reader import read_input_from_file


def binary_search_bound(time, distance, lower_bound=True):
    low = 0
    high = time
    while low <= high:
        mid = (low + high) // 2
        if (time - mid) * mid >= distance:
            if lower_bound:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if lower_bound:
                low = mid + 1
            else:
                high = mid - 1
    return low if lower_bound else high + 1


def find_race_solutions(time, distance):
    return binary_search_bound(time, distance, lower_bound=False) - binary_search_bound(time, distance)


def prod_races(races: list):
    solutions_product = 1
    for time, distance in races:
        solutions_product *= find_race_solutions(time, distance)
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
