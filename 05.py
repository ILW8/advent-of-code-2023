from collections import defaultdict
from input_reader import read_input_from_file


def get_overlap(range_left, range_right):
    return range(max(range_left.start, range_right.start), min(range_left.stop, range_right.stop))


def not_contained_in(test_range: range, other_ranges: set):
    for other_range in other_ranges:
        if len(get_overlap(test_range, other_range)):
            return False
    return True


def search_mappings(maps: dict, map_name: str, source_val: range):
    # first split input range into different matching range maps
    input_split = set()
    for key in maps[map_name].keys():
        overlap = get_overlap(key, source_val)
        if len(overlap):
            input_split.add(overlap)

    # if no overlap at all, return as is
    if not len(input_split):
        return {source_val}

    # perform mapping
    output_ranges = set()
    for input_mapped_range in input_split:
        for key in maps[map_name].keys():
            if not len(get_overlap(input_mapped_range, key)):
                continue
            range_len = input_mapped_range.stop - input_mapped_range.start
            dest_start = input_mapped_range.start - key.start + maps[map_name][key]
            output_ranges.add(range(dest_start, dest_start + range_len))

    # pass through the rest of the unmapped ranges
    remaining_input_split = set()
    for input_mapped_range in input_split:
        if len(get_overlap(source_val, input_mapped_range)):
            new_left = range(source_val.start, input_mapped_range.start)
            if len(new_left) and not_contained_in(new_left, input_split):
                remaining_input_split.add(new_left)
            new_right = range(input_mapped_range.stop, source_val.stop)
            if len(new_right) and not_contained_in(new_right, input_split):
                remaining_input_split.add(new_right)

    return output_ranges.union(remaining_input_split)


def main(input_data: list):
    seeds = list(map(int, input_data[0][6:].split()))
    seed_pairs = list(zip(seeds[::2], seeds[1::2]))
    maps = defaultdict(dict)
    current_map = None

    for line in input_data[1:]:
        if "map:" in line:
            current_map = line[:-5]
            continue
        if current_map is None or not line:
            continue

        dest, src, length = map(int, line.split())
        maps[current_map][range(src, src + length)] = dest

    min_loc = None
    for pair in seed_pairs:
        map_names = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light",
                     "light-to-temperature", "temperature-to-humidity", "humidity-to-location"]

        results = [range(pair[0], pair[0] + pair[1])]
        for map_name in map_names:
            new_results = []
            for interval in results:
                new_results.extend(search_mappings(maps, map_name, interval))
            results = new_results

        for r in results:
            if min_loc is None or r.start < min_loc:
                min_loc = r.start
    print(min_loc)


if __name__ == '__main__':
    main(read_input_from_file("05.txt"))
