import sys
import os
import re
from queue import SimpleQueue


sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/18

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

NEIGHBOURS_3D = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
]

FACES = 6


def read_input(input_file):
    def parse(s):
        return tuple(map(int, re.findall(r'\d+', s)))

    return list(map(parse, read_file_str(input_file, True)))


#  Two 1×1×1 cubes are face-adjacent if they differ by exactly 1 along
#  one axis and are identical along the other two.
#  So if cube A is at (x1, y1, z1) and cube B at (x2, y2, z2):
#  They are adjacent iff
#     |x1 - x2| + |y1 - y2| + |z1 - z2| == 1
def face_adjacent(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1


def bounds(cubes):
    xs = [x for x, _, _ in cubes]
    ys = [y for _, y, _ in cubes]
    zs = [z for _, _, z in cubes]

    min_x, max_x = min(xs)-1, max(xs)+1
    min_y, max_y = min(ys)-1, max(ys)+1
    min_z, max_z = min(zs)-1, max(zs)+1

    return [(min_x, max_x), (min_y, max_y), (min_z, max_z)]


def in_bounds(p, xyz_bounds):
    return all(xyz_bounds[i][0] <= p[i] <= xyz_bounds[i][1] for i in range(3))


def part1(input):
    result = 0

    for i in range(len(input)):
        unconnected_faces = FACES
        for j in range(len(input)):
            if i == j:
                continue

            if face_adjacent(input[i], input[j]):
                unconnected_faces -= 1

        result += unconnected_faces

    return result


def part2(input):
    xyz_bounds = bounds(input)
    x_bounds, y_bounds, z_bounds = xyz_bounds

    visited = set()
    q = SimpleQueue()

    # start with min x, y, z
    q.put((x_bounds[0], y_bounds[0], z_bounds[0]))

    # flood fill
    while not q.empty():
        p = q.get()
        if in_bounds(p, xyz_bounds) and p not in visited and p not in input:
            visited.add(p)

            for delta in NEIGHBOURS_3D:
                q.put((p[0] + delta[0], p[1] + delta[1], p[2] + delta[2]))

    # enclosed air
    enclosed = set()
    for x in range(x_bounds[0]+1, x_bounds[1]):
        for y in range(y_bounds[0]+1, y_bounds[1]):
            for z in range(z_bounds[0]+1, z_bounds[1]):
                p = (x, y, z)
                if p not in visited and p not in input:
                    enclosed.add(p)

    return part1(input) - part1(list(enclosed))


def main():
    input = read_input("../data/day18.txt")
    test_input = read_input("../data/day18-test.txt")

    assert (res := part1(test_input)) == 64, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 3650

    assert (res := part2(test_input)) == 58, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 2118


if __name__ == '__main__':
    main()
