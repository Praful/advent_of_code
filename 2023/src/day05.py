from collections import OrderedDict
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/05

#  D  S  C
#  50 98 2
#  52 50 48
# line 1: Dest 50, Source 98, Count 2; => 98 -> 50, 99 -> 51
# unmapped source numbers correspond to same destination, eg seed 10 maps to
# destination 10 if no mapping


class Almanac:
    def __init__(self):
        self.mappings = OrderedDict()

    def add_mapping(self, name, mapping):
        self.mappings[name] = mapping

    # Part 1: we search in order, starting with seed-to-soil map
    # and ending with humidity-to-location map
    def seed_location(self, seed):
        source = seed
        for name, mappings in self.mappings.items():
            for mapping in mappings:
                v = mapping.find_dest(source)
                if v is not None:
                    source = v
                    break

        return source

    def create_seed_ranges(self, seeds):
        result = []
        for i in range(0, len(seeds), 2):
            start = seeds[i]
            count = seeds[i+1]
            result.append(range(start, start+count))
        return result

    def in_seed_ranges(self, target, ranges):
        for r in ranges:
            if target in r:
                return True
        return False

    # Part 2: we search in reverse order, starting with humidity-to-location map
    # and ending with seed-to-soil map. That's because we try all locations starting
    # with 0 and increasing until a seed is found in the range of seeds provided.
    # Reading reddit afterwards, I saw that a common (and faster) solution was to check
    # for the intersection of ranges so that some destinations can be eliminated.
    def min_seed_location(self, seeds):
        seed_ranges = self.create_seed_ranges(seeds)

        reversed_mapping = OrderedDict(reversed(list(self.mappings.items())))

        location = 0

        while True:
            #  if location % 200000 == 0:
                #  print(location)

            dest = location

            for name, mappings in reversed_mapping.items():
                for mapping in mappings:
                    v = mapping.find_source(dest)
                    if v is not None:
                        dest = v
                        break

            if self.in_seed_ranges(dest, seed_ranges):
                return location
            else:
                location += 1


class Mapping:
    def __init__(self, dest, source, count):
        self.dest = dest
        self.source = source
        self.count = count

    def __str__(self):
        return f'source {self.source} -> dest {self.dest}, count {self.count}'

    def __repr__(self):
        return str(self)

    def find_dest(self, source):
        r = range(self.source, self.source + self.count)
        if source in r:
            i = r.index(source)
            return self.dest + i
        else:
            return None

    def find_source(self, dest):
        r = range(self.dest, self.dest + self.count)
        if dest in r:
            i = r.index(dest)
            return self.source + i
        else:
            return None


def read_input(input_file):
    input = read_file_str(input_file, True)

    seeds = list(map(int, input[0].split(':')[1].split()))
    almanac = Almanac()
    mappings = []
    name = ''
    for i, line in enumerate(input):
        if i == 0:
            continue

        # blank line means end of mapping
        if is_blank(line):
            if mappings:
                almanac.add_mapping(name, mappings)

            mappings = []
            name = ''
            continue

        # Are we on a new mapping eg soil-to-fertilizer map
        if line.endswith('map:') > 0:
            name = line.split('map:')[0].strip()
            continue

        # ok we have an actual mapping
        mappings.append(Mapping(*list(map(int, line.split()))))

    almanac.add_mapping(name, mappings)

    return (seeds, almanac)


def part1(input):
    seeds = input[0]
    almanac = input[1]

    return min(map(almanac.seed_location, seeds))


# This takes about 10 minutes to run on a i7-6700K with my input; not fast but good enough!
def part2(input):
    seeds = input[0]
    almanac = input[1]

    return almanac.min_seed_location(seeds)


# This takes too long to run for real input.
def part2_brute_force(input):
    seeds = input[0]
    almanac = input[1]

    locations = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        count = seeds[i+1]
        for seed in range(start, start+count):
            locations.append(almanac.seed_location(seed))

    return min(locations)


def main():
    input = read_input("../data/day05.txt")
    test_input = read_input("../data/day05-test.txt")

    assert (res := part1(test_input)) == 35, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 424490994

    assert (res := part2_brute_force(test_input)) == 46, f'Actual: {res}'
    assert (res := part2(test_input)) == 46, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 15290096


if __name__ == '__main__':
    main()
