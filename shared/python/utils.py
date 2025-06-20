from enum import Enum
import numpy as np
import math
import re


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


# Unless otherwise specified, all directions are represented by a tuple (row, col) ie y, x.
# This to make it easier to reference lists.
NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
NORTHEAST = (-1, 1)
SOUTHEAST = (1, 1)
SOUTHWEST = (1, -1)
NORTHWEST = (-1, -1)

# Clockwise 90 degrees
ROTATE = {
    EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST
}


DIRECTIONS_ALL = [
    NORTH,
    EAST,
    SOUTH,
    WEST,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
]

DIRECTION_DELTAS = {
    # (row, col)
    Direction.EAST: EAST,
    Direction.NORTH: NORTH,
    Direction.WEST: WEST,
    Direction.SOUTH: SOUTH
}

ARROWS_TO_DIRECTION = {
    '>': Direction.EAST,
    'v': Direction.SOUTH,
    '<': Direction.WEST,
    '^': Direction.NORTH,
}

ARROWS_TO_DIRECTION2 = {
    '>': EAST,
    'v': SOUTH,
    '<': WEST,
    '^': NORTH,
}

DIRECTION2_TO_ARROWS = {
    EAST: '>',
    SOUTH: 'v',
    WEST: '<',
    NORTH: '^',
}


def into_range(x, n, m):
    # for x returns value in range n-m (inclusive)
    return ((x-n) % (m-n+1))+n


def next_neighbour(position, direction):
    return (position[0] + DIRECTION_DELTAS[direction][0], position[1] + DIRECTION_DELTAS[direction][1])


def next_neighbour2(position, direction):
    # a faster version if direction is stored as tuple instead of enum
    return (position[0] + direction[0], position[1] + direction[1])


def in_grid(position, grid):
    return 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0])


def tile(grid, p):
    return grid[p[0]][p[1]]


def add_pos(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def subtract_pos(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


direction = subtract_pos


def print_grid(grid, axis=False):
    if axis:
        print('  ' + ''.join([str(i % 10) for i in range(len(grid[0]))]))

    for r, row in enumerate(grid):
        if axis:
            print(r % 10, end=' ')
        print(''.join(row))


def make_grid(rows, cols, value=0):
    #  return np.array([[point(x, y) for x in range(cols)] for y in range(rows)])
    return [[value] * cols for _ in range(rows)]


# return all positions of value in grid
def find_in_grid(grid, value):
    result = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == value:
                result.append((i, j))

    return result


def neighbours(position, grid, check_in_bounds=True, condition=lambda g, x: True):
    def in_grid_bound(p):
        if check_in_bounds:
            return in_grid(p, grid)
        else:
            return True

    result = []
    for d in DIRECTION_DELTAS.keys():
        new_position = next_neighbour(position, d)
        if in_grid_bound(new_position) and condition(grid, new_position):
            result.append(new_position)

    return result


def reverse_direction(direction):
    if direction == Direction.EAST:
        return Direction.WEST
    if direction == Direction.WEST:
        return Direction.EAST
    if direction == Direction.NORTH:
        return Direction.SOUTH
    if direction == Direction.SOUTH:
        return Direction.NORTH


# rotate 90 degrees clockwise or anticlockwise
def rotate_direction(current_direction, anticlockwise=False):
    directions = list(Direction)

    # Determine the step: +1 for clockwise, -1 for anticlockwise
    step = -1 if anticlockwise else 1

    # Calculate the next index using modular arithmetic
    next_index = (current_direction.value + step) % len(directions)
    return directions[next_index]


class Direction2(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def read_file_str(filename, strip=False):
    """ return list of strings, one line per list entry"""
    result = []
    with open(filename) as f:
        for line in f:
            l = line
            if strip:
                l = line.strip()
            result.append(l)

    return result


def read_file_int(filename):
    """ file consists of a rows of numbers"""
    result = []
    with open(filename) as f:
        for line in f:
            result.append(list(map(int, line.split())))

    return result


def extract_ints(s):
    return map(int, re.findall(r'\d+', s))


def lcm(l):
    #  https://en.wikipedia.org/wiki/Least_common_multiple
    result = 1
    for n in l:
        result = (n*result) // math.gcd(n, result)
    return result


# Boolean, unsigned integer, signed integer, float, complex.
NUMERIC_KINDS = set('buifc')
NOT_NUMERIC = [object(), 'string', u'unicode', None]


def replace(s, index, new_char):
    """ change single char at index in string s """
    return s[:index] + new_char + s[index + 1:]


def is_blank(s):
    """ Return true if string is not defined or empty"""
    return not (s and s.strip())


def is_numeric(array):
    return np.asarray(array).dtype.kind in NUMERIC_KINDS


def is_valid(enum, s):
    """ checks if s is a valid value for an enum class"""
    for l in list(enum):
        if l.value == s:
            return True

    return False

# Example:
#  sequence = (-9, 0, 5, 9, -1)  # Example sequence of length n = 5
#  encoded = encode_sequence(sequence, 18, 9)
#  print(f"Encoded: {encoded}")

#  decoded = decode_sequence(encoded, len(sequence), 18, 9)
#  print(f"Decoded: {decoded}")


# Encodes a sequence of n numbers into a single integer.
def encode_sequence(sequence, base, offset):
    encoded = 0
    n = len(sequence)
    for i, num in enumerate(sequence):
        # Add (num + offset) at the appropriate base position
        encoded += (num + offset) * (base ** (n - i - 1))
    return encoded


#  Decodes a single integer back into the original sequence of n numbers.
def decode_sequence(encoded, n, base, offset):

    sequence = []
    for i in range(n):
        # Extract the digit at the current position
        digit = (encoded // (base ** (n - i - 1))) % BASE
        # Shift back to the original range
        sequence.append(digit - offset)
    return tuple(sequence)


def to_numpy_array(a):
    # Turn list of strings into 2D numpy array with one character per cell

    rows = [list(l) for l in a]
    return np.array(rows, str)


def chunk_string(s, chunk_size):
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]


def print_np_info(a):
    print('size: ', a.size)
    print('shape: ', a.shape)
    if is_numeric(a):
        print('max:', a.max(axis=0))
        print('min:', a.min(axis=0))


def determinant(p1, p2):
    #  print(p1, p2)
    return p1[0] * p2[1] - p1[1] * p2[0]


def internal_area(boundary_points, boundary_length):
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # Pick's theorem: total area = internal_area + boundary_length/2 - 1
    # We have the boundary points and need the internal area.
    # Rearranging, we get: internal_area = area + 1 - boundary_length/2
    # We use the shoelace formula to get the total area
    return (shoelace_area(boundary_points) + 1 - boundary_length / 2)


def shoelace_area(input):
    # https://en.wikipedia.org/wiki/Shoelace_formula

    area = 0
    for i in range(len(input)):
        p1 = input[i]
        p2 = input[(i + 1) % len(input)]
        area += determinant(p1, p2)

    return abs(area)/2


def hex_to_dec(s):
    return int(s, 16)

# class Point:
#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y
#         np.array

#     def __eq__(self, other):
#         if isinstance(other, Point):
#             return self.x == other.x and self.y == other.y
#         return False

#     def __hash__(self) -> int:
#         return hash((self.x, self.y))

#     def __add__(self, other):
#         return self.add(other)

#     def add(self, p, count=1):
#         return Point(self.x + (p.x * count), self.y + (p.y * count))

#     def __repr__(self):
#         return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

#     def distance_from_origin(self):
#         return ((self.x ** 2) + (self.y ** 2)) ** 0.5

#     def print_point(self):
#         print('({0}, {1})'.format(self.x, self.y))

#     def distanceFromOrigin(self):
#         origin = Point(0, 0)
#         dist = self.distanceFromPoint(origin)
#         return dist

#     def distanceFromPoint(self, point):
#         return math.sqrt(self.x - point.x)**2 + (self.y - point.y)**2

#     def is_adjacent(self, p, include_diagonal=True):
#         adj = ADJACENT_DIAG if include_diagonal else ADJACENT
#         return any([self + a == p for a in adj])


def point(x=0, y=0):
    return np.array([x, y])


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return abs(x2 - x1) + abs(y2 - y1)


def is_adjacent(p1, p2, include_diagonal=True):
    adj = ADJACENT_DIAG if include_diagonal else ADJACENT
    return any([np.array_equal(p1 + a, p2) for a in adj])


ADJACENT = [point(0, 1), point(0, -1), point(1, 0), point(-1, 0)]
ADJACENT_DIAG = [*ADJACENT,
                 point(1, 1), point(1, -1), point(-1, 1), point(-1, -1)]

# provide equation of line coefficients (A, B, C) for Ax+By=C


def intersection_point(line1, line2):

    A = np.array([line1[:2], line2[:2]])
    b = np.array([line1[2], line2[2]])
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None  # Lines are parallel


# return A, B, C for Ax+By=C
def equation_of_line_coefficients(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # m = slope
    if x2 - x1 != 0:  # Avoid div by zero
        m = (y2 - y1) / (x2 - x1)
    else:
        m = float('inf')  # Vertical line

    # Use one of the points to find the equation
    # For vertical lines (x2 - x1 == 0), the equation is x = x1
    if m != float('inf'):
        C = y1 - m * x1
        #  equation = f'y = {m}x + {b}'
        B = 1
        A = -m
    else:
        C = 0
        #  equation = f'x = {x1}'
        B = 0
        A = x1

    return (A, B, C)


def rgb(r, g, b):
    # for printing coloured text in a terminal
    return f"\033[38;2;{r};{g};{b}m"


def rgb_bg(r, g, b):
    # for printing coloured text in a terminal
    return f"\033[48;2;{r};{g};{b}m"


# For example usage, see ../../2023/src/day10.py. For example output, see
# ../../2023/data/day10-visualisation.txt
COLOUR_BLACK = rgb(0, 0, 0)
COLOUR_RED = rgb(255, 0, 0)
COLOUR_GREEN_BACKGROUND = rgb_bg(0, 255, 0)
COLOUR_RED_BACKGROUND = rgb_bg(255, 0, 0)
COLOUR_RESET = "\033[0m"  # always reset after changing colour


class ReprMixin:
    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v)
                           for k, v in self.__dict__.items()),
        )


class TreeNode:
    def __init__(self, value):
        self.value = value  # Value of the node
        self.children = []  # List to hold child nodes

    def add_child(self, child_value):
        """Adds a child to the current node."""
        child = TreeNode(child_value)
        self.children.append(child)
        return child  # Return the child node for further operations

    def traverse(self, level=0):
        """Recursively traverse the tree and print it."""
        print("  " * level + str(self.value))  # Indent based on tree level
        for child in self.children:
            child.traverse(level + 1)  # Traverse children with increased level

    def get_all_paths(self, path=""):
        """Returns all paths from root to each leaf as a list of strings."""
        current_path = path + self.value
        if not self.children:
            # Leaf node, return the path as a single-item list
            return [current_path]

        paths = []
        for child in self.children:
            paths.extend(child.get_all_paths(current_path))
        return paths

    def __str__(self):
        return self.value


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_after(self, prev_node, data):
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        return new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def update(self, node, data):
        node.data = data

    def delete(self, data):
        current = self.head
        if current and current.data == data:
            self.head = current.next
            return
        previous = None
        while current and current.data != data:
            previous = current
            current = current.next
        if current:
            previous.next = current.next

    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    @property
    def count(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
