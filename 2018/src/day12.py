import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict

# Puzzle description: https://adventofcode.com/2018/day/12


def plant_score(pots, centre_plant_id):
    return sum([i - centre_plant_id + 1 for i, v in enumerate(pots) if v == PLANT])


PLANT = '#'
EMPTY = '.'


# set do_print to True for diagnosis for part 2 to see
# pattern
def generate(input, num_gen=20, do_print=False):

    CENTRE_PLANT_ID = 5
    plants = EMPTY * (CENTRE_PLANT_ID - 1) + input[0] + EMPTY * 5
    num_plants = len(plants)
    PADDING = EMPTY * 5
    PADDING_SIZE = len(PADDING)
    rules = input[1]
    new_score = 0

    for gen in range(1, num_gen + 1):
        next_gen = EMPTY * 2
        for i in range(2, len(plants) - 2):

            p = plants[i - 2:i + 3]
            r = rules.get(p, EMPTY)
            next_gen += r

        plants = next_gen.ljust(num_plants, EMPTY)

        # make sure we have enough empty pots to the left and right
        if plants[0:PADDING_SIZE] != PADDING:
            plants = PADDING + plants
            CENTRE_PLANT_ID += PADDING_SIZE

        if plants[len(plants) - PADDING_SIZE:] != PADDING:
            plants = plants + PADDING

        if do_print:
            old_score = new_score
            new_score = plant_score(plants, CENTRE_PLANT_ID)
            print(gen, new_score, new_score - old_score)

    return plant_score(plants, CENTRE_PLANT_ID)


def read_input(input_file):
    input = utils.read_file_str(input_file)
    initial_state = (input[0].split('initial state: ')[1]).strip()
    rules = defaultdict()
    for i in range(2, len(input)):
        r = input[i].split(' => ')
        rules[r[0]] = r[1].strip()

    return (initial_state, rules)


def main():
    main_input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")

    # print(f'Part 1 (test) {generate(test_input)}')  # 325
    print(f'Part 1 {generate(main_input)}')  # 2911

    # Look for pattern: in our case this begins at generation
    # 90, after which the score increases by 50 per geneeration
    # print(f'Part 2 {generate(main_input, 200, True)}')  #
    print(f'Part 2 {generate(main_input, 90)+int(5e10-90)*50}')


if __name__ == '__main__':
    main()
