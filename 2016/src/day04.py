import sys
import os
from collections import Counter

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/4

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(s):
        s2 = s.split('[')
        checksum = s2[1][:-1]
        s3 = s2[0].split('-')
        name = s3[:-1]
        sector_id = int(s3[-1])
        return name, checksum, sector_id

    input = map(parse, read_file_str(input_file, True))
    return list(input)


def most_common(a, n):
    # Counter returns in order of most frequent; where there's a tie,
    # sort alphabetically eg ('a', 2) before ('b', 2)
    # sorted sorts by ascending; the -x[1] makes it descending for first key (number)
    # and ascending for second key (letter)
    return sorted(
        Counter(a).items(),
        key=lambda x: (-x[1], x[0])
    )[:n]


def is_real_room(name, checksum):
    common = most_common(''.join(name), 5)
    derived_checksum = ''.join(c[0] for c in common)
    return derived_checksum == checksum


def part1(input):
    result = 0
    for name, checksum, sector_id in input:
        if is_real_room(name, checksum):
            result += sector_id
    return result


def decrypt(name, sector_id):
    # increment c by sector_id times
    def decrypt_char(c):
        return chr((ord(c) - ord('a') + sector_id) % 26 + ord('a'))

    result = []
    for s in name:
        decrypted_s = [decrypt_char(c) for c in s]
        result.append(''.join(decrypted_s))

    return ' '.join(result)


def part2(input):
    for name, checksum, sector_id in input:
        if is_real_room(name, checksum):
            if decrypt(name, sector_id) == 'northpole object storage':
                return sector_id

    assert False, 'Not found'


def main():
    input = read_input("../data/day04.txt")
    test_input = read_input("../data/day04-test.txt")

    assert (res := part1(test_input)) == 1514, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 158835

    assert (res := decrypt(['qzmt', 'zixmtkozy', 'ivhz'], 343)
            ) == 'very encrypted name', f'Actual: {res}'  #

    print(f'Part 2 {part2(input)}')  # 993


if __name__ == '__main__':
    main()
