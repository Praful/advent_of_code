from enum import Enum
import numpy as np
import math


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


DIRECTIONS_ALL = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),]

DIRECTION_DELTAS = {
    # (col, row)
    Direction.EAST: (1, 0),
    Direction.NORTH: (0, -1),
    Direction.WEST: (-1, 0),
    Direction.SOUTH: (0, 1),
}

ARROWS_TO_DIRECTION = {
    '>': Direction.EAST,
    'v': Direction.SOUTH,
    '<': Direction.WEST,
    '^': Direction.NORTH,
}


def into_range(x, n, m):
    # for x returns value in range n-m (inclusive)
    return ((x-n) % (m-n+1))+n


def next_neighbour(position, direction):
    return (position[0] + DIRECTION_DELTAS[direction][0], position[1] + DIRECTION_DELTAS[direction][1])

def in_grid(p, grid):
    return 0 <= p[0] < len(grid[0]) and 0 <= p[1] < len(grid)


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
    """ change single char in string s """
    l = list(s)
    l[index] = new_char
    return ''.join(l)


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


def to_numpy_array(a):
    # Turn list of strings into 2D numpy array with one character per cell

    rows = [list(l) for l in a]
    return np.array(rows, str)


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


def make_grid(rows, cols, value=0):
    #  return np.array([[point(x, y) for x in range(cols)] for y in range(rows)])
    return [[value] * cols for _ in range(rows)]


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
