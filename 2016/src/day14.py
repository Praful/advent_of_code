import re
from collections import defaultdict

from utils import md5_hash

# Puzzle description: https://adventofcode.com/2024/day/XX

#  DEBUG = True
DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def has_three_matches(s):
    match = re.search(r"(.)\1{2}", s)

    if match:
        return match.group(1)

    return None


def five_matches(s):
    return re.findall(r"(.)\1{4}", s)


def generate_keys(salt, part2=False):

    def finished():
        # We can just wait until we've found 64 keys because candidate keys are not
        # found in order eg candidate index 200 could be found before candidate index 100.
        # Therefore we have to make sure a lower candidate index is not going to be a key.
        # We do that by waiting until a 1000 index gap has passed
        return len(found_key_indexes) >= 64 and index - found_key_indexes[63] > 1000

    index = 0
    three_matches = defaultdict(list)
    found_key_indexes = []

    while not finished():
        hash = md5_hash(salt + str(index))

        if part2:
            for _ in range(2016):
                hash = md5_hash(hash)

        for five_ch in five_matches(hash):
            for threes in three_matches[five_ch]:
                if index - threes[1] <= 1000:
                    found_key_indexes.append(threes[1])
            found_key_indexes.sort()
            three_matches[five_ch] = []

        three_ch = has_three_matches(hash)
        if three_ch is not None:
            print_debug("triple", index, three_ch, hash)
            three_matches[three_ch].append((three_ch, index))

        index += 1

    return found_key_indexes[63]


def part1(input):
    return generate_keys(input)


def part2(input):
    return generate_keys(input, True)


def main():
    input = "cuanljph"
    test_input = "abc"

    assert (res := part1(test_input)) == 22728, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 23769
    assert (res := part2(test_input)) == 22551, f"Actual: {res}"
    print(f"Part 2 {part2(input)}")  # 20606


if __name__ == "__main__":
    main()
