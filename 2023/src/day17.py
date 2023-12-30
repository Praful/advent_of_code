from dataclasses import dataclass
import os
import sys
from queue import PriorityQueue
from queue import SimpleQueue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/17


@dataclass
class Crucible:
    position: tuple
    blocks_moved: int
    heat_loss: int
    direction: Direction

    def __hash__(self):
        return hash((self.position, self.blocks_moved, self.heat_loss, self.direction))

    def __repr__(self):
        return f'Crucible({self.position}, {self.blocks_moved}, {self.heat_loss}, {self.direction})'

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


def read_input(input_file):
    return read_file_str(input_file, True)


def adjacent_tiles(grid, crucible, min_blocks, max_blocks):
    def in_grid(pos):
        return 0 <= pos[0] < len(grid[0]) and 0 <= pos[1] < len(grid)

    result = []

    for new_dir in DIRECTION_DELTAS:
        if new_dir == reverse_direction(crucible.direction):
            continue

        new_position = (crucible.position[0] + DIRECTION_DELTAS[new_dir][0],
                        crucible.position[1] + DIRECTION_DELTAS[new_dir][1])

        if not in_grid(new_position):
            continue

        blocks_moved = 1

        if new_dir == crucible.direction:
            if crucible.blocks_moved >= max_blocks:
                continue

            blocks_moved = crucible.blocks_moved + 1

        elif crucible.blocks_moved < min_blocks:
            continue

        tile_heat_loss = int(grid[new_position[1]][new_position[0]])

        result.append(Crucible(new_position, blocks_moved,
                      crucible.heat_loss + tile_heat_loss, new_dir))

    return result


def bfs(input, min_blocks=0, max_blocks=3):
    # Using BFS algorithm:
    # https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-breadth-first 
    # This is almost identical to A* below except that it finds all possible paths
    # between start and finish by using a simple queue and storing heat loss results. The 
    # upshot is that it's extremely slow!
    # In contrast, A* priortises the lowest cost path during traversal and therefore
    # doesn't visit every node.
    # I wrote this to see how slow bfs is after solving using A*.

    finish_pos = (len(input[0]) - 1, len(input) - 1)
    heat_loss_so_far = {}
    result = []
    
    q = SimpleQueue()
    q.put(Crucible((0, 0), 0, 0, Direction.EAST))
    q.put(Crucible((0, 0), 0, 0, Direction.SOUTH))

    while not q.empty():
        crucible = q.get()

        for adj in adjacent_tiles(input, crucible, min_blocks, max_blocks):
            if adj.position == finish_pos and adj.blocks_moved >= min_blocks:
                result.append(adj.heat_loss) 
                continue

            key = (adj.position, adj.blocks_moved, adj.direction)

            if key not in heat_loss_so_far or adj.heat_loss < heat_loss_so_far[key]:
                heat_loss_so_far[key] = adj.heat_loss
                q.put(adj)

    return min(result)

def traverse(input, min_blocks=0, max_blocks=3):
    # Using A* algorithm: https://www.redblobgames.com/pathfinding/a-star/introduction.html#astar

    #  return bfs(input, min_blocks, max_blocks)

    finish_pos = (len(input[0]) - 1, len(input) - 1)

    q = PriorityQueue()
    q.put(Crucible((0, 0), 0, 0, Direction.EAST))
    q.put(Crucible((0, 0), 0, 0, Direction.SOUTH))

    heat_loss_so_far = {}

    while not q.empty():
        crucible = q.get()

        for adj in adjacent_tiles(input, crucible, min_blocks, max_blocks):
            if adj.position == finish_pos and adj.blocks_moved >= min_blocks:
                return adj.heat_loss

            key = (adj.position, adj.blocks_moved, adj.direction)

            if key not in heat_loss_so_far or adj.heat_loss < heat_loss_so_far[key]:
                heat_loss_so_far[key] = adj.heat_loss
                q.put(adj)

    raise Exception('No path found')


def part1(input):
    return traverse(input)


def part2(input):
    return traverse(input, 4, 10)


def main():
    input = read_input("../data/day17.txt")
    test_input1 = read_input("../data/day17-test-1.txt")
    test_input2 = read_input("../data/day17-test-2.txt")

    assert (res := part1(test_input1)) == 102, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1110

    assert (res := part2(test_input1)) == 94, f'Actual: {res}'
    assert (res := part2(test_input2)) == 71, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1294


if __name__ == '__main__':
    main()
