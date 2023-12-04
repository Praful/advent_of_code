import re
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/2


def read_input(input_file):
    input = read_file_str(input_file, True)
    return parse_input(input)

class Game:
    def __init__(self, id, cubes):
        self.id = id
        self.cubes = cubes
    def __str__(self):
        return str(self.id) + ': ' + str(self.cubes)
    def __repr__(self):
        return str(self)

def parse_input(input):
    games = []
    for game in input:
        id = int(re.findall(r'\d+', game.split(': ')[0])[0])
        cubes_str = (game.split(': ')[1]).split('; ')
        cubes = []
        for cube_sets in cubes_str:
            colours = cube_sets.split(', ')
            cube_set = {'red': 0, 'green': 0, 'blue': 0} 

            for colour in colours:
                colour_part = colour.split(' ')
                cube_set[colour_part[1]] = int(colour_part[0])
            cubes.append(cube_set)
        
        games.append(Game(id, cubes))

    return games



def part1(input, rgb):
    result = 0
    
    for game in input:
        playable_games = sum(1 for cube in game.cubes
                            if cube['red'] <= rgb[0] and cube['green'] <= rgb[1] and cube['blue'] <= rgb[2])

        if len(game.cubes) == playable_games:
            result += game.id

    return result


def part2(input):
    result = 0

    for game in input:
        min_cube = {'red': 0, 'green': 0, 'blue': 0}
        for cube in game.cubes:
            if cube['red'] > min_cube['red']:
                min_cube['red'] = cube['red']
            if cube['green'] > min_cube['green']:
                min_cube['green'] = cube['green']
            if cube['blue'] > min_cube['blue']:
                min_cube['blue'] = cube['blue']

        result += min_cube['red'] * min_cube['green'] * min_cube['blue']

    return result

def main():
    input = read_input("../data/day02.txt")
    test_input = read_input("../data/day02-test.txt")

    assert (res := part1(test_input, (12,13,14))) == 8, f'Actual: {res}'

    print(f'Part 1 {part1(input, (12,13,14))}')  # 1734

    assert (res := part2(test_input)) == 2286, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 70387


if __name__ == '__main__':
    main()
