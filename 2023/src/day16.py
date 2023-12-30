from dataclasses import dataclass
import os
import sys
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/16

DIRECTION_DELTAS = {
    # (col, row)
    Direction.EAST: (1, 0),
    Direction.NORTH: (0, -1),
    Direction.WEST: (-1, 0),
    Direction.SOUTH: (0, 1),
}

@dataclass
class Beam:
    position: tuple
    direction: Direction

    def next_position(self):
        return self.position[0] + DIRECTION_DELTAS[self.direction][0], self.position[1] + DIRECTION_DELTAS[self.direction][1]

    def __repr__(self):
        return f'Beam({self.position}, {self.direction})'

    def __hash__(self):
        return hash((self.position, self.direction))


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input



def next_step(grid, beam):
    def in_grid(b):
        return 0 <= b.position[0] < len(grid[0]) and 0 <= b.position[1] < len(grid)

    def add_beam(b=None):
        if b is None:
            b = Beam(beam.next_position(), beam.direction)

        if in_grid(b):
            result.append(b)

    result = []
    tile = grid[beam.position[1]][beam.position[0]]

    match tile:
        case ".":
            add_beam()
        case '|':
            if beam.direction in [Direction.EAST, Direction.WEST]:
                # split beam
                next_position = Beam(beam.position, Direction.NORTH).next_position()
                add_beam(Beam(next_position, Direction.NORTH))
                next_position = Beam(beam.position, Direction.SOUTH).next_position()
                add_beam(Beam(next_position, Direction.SOUTH))
            else:
                add_beam()
        case '-':
            if beam.direction in [Direction.NORTH, Direction.SOUTH]:
                # split beam
                next_position = Beam(beam.position, Direction.EAST).next_position()
                add_beam(Beam(next_position, Direction.EAST))
                next_position = Beam(beam.position, Direction.WEST).next_position()
                add_beam(Beam(next_position, Direction.WEST))
            else:
                add_beam()
        case '\\':
            if beam.direction  == Direction.NORTH:
                next_position = Beam(beam.position, Direction.WEST).next_position()
                add_beam(Beam(next_position, Direction.WEST))
            if beam.direction  == Direction.SOUTH:
                next_position = Beam(beam.position, Direction.EAST).next_position()
                add_beam(Beam(next_position, Direction.EAST))
            if beam.direction  == Direction.EAST:
                next_position = Beam(beam.position, Direction.SOUTH).next_position()
                add_beam(Beam(next_position, Direction.SOUTH))
            if beam.direction  == Direction.WEST:
                next_position = Beam(beam.position, Direction.NORTH).next_position()
                add_beam(Beam(next_position, Direction.NORTH))
        case '/':
            if beam.direction  == Direction.NORTH:
                next_position = Beam(beam.position, Direction.EAST).next_position()
                add_beam(Beam(next_position, Direction.EAST))
            if beam.direction  == Direction.SOUTH:
                next_position = Beam(beam.position, Direction.WEST).next_position()
                add_beam(Beam(next_position, Direction.WEST))
            if beam.direction  == Direction.EAST:
                next_position = Beam(beam.position, Direction.NORTH).next_position()
                add_beam(Beam(next_position, Direction.NORTH))
            if beam.direction  == Direction.WEST:
                next_position = Beam(beam.position, Direction.SOUTH).next_position()
                add_beam(Beam(next_position, Direction.SOUTH))
        case _:
            raise Exception(f'Unknown tile: {tile} for beam {beam}')

    return result

def part1(input):
    return energise_tiles(input)

def energise_tiles(input, beam=Beam((0, 0), Direction.EAST)):
    energised = set()

    # store beams so that we don't repeat their paths
    visited = set()
    
    # q contains the travelling beams 
    q = queue.SimpleQueue()
    q.put(beam)

    while not q.empty():
        beam = q.get()
        energised.add(beam.position)

        for beam in next_step(input, beam):
            if beam in visited:
                continue
            else:
                visited.add(beam)
                q.put(beam)

    return len(energised)


def part2(input):
    result = 0

    for col in range(len(input[0])):
        result = max(result, energise_tiles(input, Beam((col, 0), Direction.SOUTH)))
        result = max(result, energise_tiles(input, Beam((col, len(input)-1), Direction.NORTH)))

    for row in range(len(input)):
        result = max(result, energise_tiles(input, Beam((0, row), Direction.EAST)))
        result = max(result, energise_tiles(input, Beam((len(input[0])-1, row), Direction.WEST)))

    return result


def main():
    input = read_input("../data/day16.txt")
    test_input = read_input("../data/day16-test.txt")

    assert (res := part1(test_input)) == 46, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 7185

    assert (res := part2(test_input)) == 51, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 7616


if __name__ == '__main__':
    main()
