import sys
import os
import json

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/12

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    with open(input_file) as f:
        input = json.load(f)
    return input

def json_values_count(obj, part2=False):
    result = 0
    if isinstance(obj, dict):
        if part2 and 'red' in obj.values():
            return 0
        for key, value in obj.items():
            #  print(f"Key: {key}")
            result += json_values_count(value, part2)
    elif isinstance(obj, list):
        for item in obj:
            result += json_values_count(item, part2)
    else:
        #  print(f"Value: {obj}")
        if isinstance(obj, int):
            result += obj

    return result

def solve(input, part2=False):
    return json_values_count(input, part2)


def main():
    input = read_input("../data/day12.txt")

    assert (res := solve([1,2,3])) == 6, f'Actual: {res}'
    assert (res := solve({"a":2,"b":4})) == 6, f'Actual: {res}'
    assert (res := solve([[[3]]] )) == 3, f'Actual: {res}'
    assert (res := solve({"a":{"b":4},"c":-1})) == 3, f'Actual: {res}'
    assert (res := solve({"a":[-1,1]})) == 0, f'Actual: {res}'
    assert (res := solve([-1,{"a":1}])) == 0, f'Actual: {res}'
    assert (res := solve([])) == 0, f'Actual: {res}'
    assert (res := solve({})) == 0, f'Actual: {res}'

    print(f'Part 1 {solve(input)}')  # 191164

    assert (res := solve([1,2,3], True)) == 6, f'Actual: {res}'
    assert (res := solve([1,{"c":"red","b":2},3], True)) == 4, f'Actual: {res}'
    assert (res := solve({"d":"red","e":[1,2,3,4],"f":5}, True)) == 0, f'Actual: {res}'
    assert (res := solve([1,"red",5], True)) == 6, f'Actual: {res}'

    print(f'Part 2 {solve(input, True)}')  # 87842
    
if __name__ == '__main__':
    main()
