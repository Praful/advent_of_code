import sys
import os
from collections import defaultdict
from collections import deque

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/22

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

PRICE_CHANGES_COUNT = 2000
PRICE_SEQUENCE_LENGTH = 4
BASE = 19  # Because the numbers range from -9 to 9
OFFSET = 9  # To shift the range from [-9, 9] to [0, 18]


def read_input(input_file):
    return [i[0] for i in read_file_int(input_file)]


def next_secret(secret):
    def mix(a, b): return a ^ b
    def prune(n): return n % 16777216

    result = mix(secret * 64, secret)
    result = prune(result)

    result = mix(result // 32, result)
    result = prune(result)

    result = mix(result*2048, result)
    return prune(result)


def secret_generator(seed, count):
    for _ in range(count):
        seed = next_secret(seed)
        yield seed


def part1(input):
    result = 0

    for secret in input:
        for s in secret_generator(secret, PRICE_CHANGES_COUNT):
            pass

        result += s

    return result


def part2(input):
    def price(n): return n % 10

    results = defaultdict(int)

    for secret in input:
        recent_prices = deque(maxlen=PRICE_SEQUENCE_LENGTH)
        previous_price = price(secret)
        recent_prices.append(previous_price)
        differences = deque(maxlen=PRICE_SEQUENCE_LENGTH)
        seen = set()
        for next_secret in secret_generator(secret, PRICE_CHANGES_COUNT):
            next_price = price(next_secret)

            recent_prices.append(next_price)
            differences.append(next_price - previous_price)

            previous_price = next_price
            # encoding the sequence to a single integer halves the time taken over
            # using the tuple as the key to results hashmap
            encoded = encode_sequence(differences, BASE, OFFSET)

            if len(differences) == PRICE_SEQUENCE_LENGTH and encoded not in seen:
                seen.add(encoded)
                results[encoded] += next_price

    return max(results.values())


def test1():
    secret = 123
    for _ in range(10):
        secret = next_secret(secret)
        print(secret)


def main():
    input = read_input("../data/day22.txt")
    test_input = read_input("../data/day22-test.txt")
    test_input2 = read_input("../data/day22-test2.txt")

    assert (res := part1(test_input)) == 37327623, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 19241711734

    assert (res := part2(test_input2)) == 23, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 2058


if __name__ == '__main__':
    main()
