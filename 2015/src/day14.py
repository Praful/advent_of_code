import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/14

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def parse(s):
    e = s.split(' ')
    return (e[0], (int(e[3]), int(e[6]), int(e[13])))


#  {'Comet': (14, 10, 127), 'Dancer': (16, 11, 162)}
def read_input(input_file):
    input = read_file_str(input_file, True)
    return dict(map(parse, input))


# return distance moved at time t
def distance_moved(t, speed, fly_time, rest_time):
    return speed if t % (fly_time + rest_time) < fly_time else 0


def total_travelled_distance(time_allowed, speed, fly_time, rest_time):
    return sum(distance_moved(t, speed, fly_time, rest_time) for t in range(time_allowed))


def part1(input, time_allowed):
    return max(map(lambda args: total_travelled_distance(time_allowed, *args), input.values()))


def part2(input, time_allowed):
    score = {}
    points = {}

    for t in range(0, time_allowed):
        for name, (speed, fly_time, rest_time) in input.items():
            score[name] = score.get(name, 0) + distance_moved(t, speed, fly_time, rest_time)

        lead_distance = max(score.values())
        for name in score.keys():
            if score[name] == lead_distance:
                points[name] = points.get(name, 0) + 1

    return max(points.values())


def main():
    time_allowed = 2503
    time_allowed_test = 1000

    input = read_input("../data/day14.txt")
    test_input = read_input("../data/day14-test.txt")

    assert (res := part1(test_input, time_allowed_test)) == 1120, f'Actual: {res}'
    print(f'Part 1 {part1(input, time_allowed)}')  # 2655

    assert (res := part2(test_input, time_allowed_test)) == 689, f'Actual: {res}'
    print(f'Part 2 {part2(input, time_allowed)}')  # 1059


if __name__ == '__main__':
    main()
