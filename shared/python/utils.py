
import numpy as np
import math


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

# Turn list of strings into 2D numpy array with one character per cell
def to_numpy_array(a):
    rows = [list(l) for l in a]
    return np.array(rows, str)


def print_np_info(a):
    print('size: ', a.size)
    print('shape: ', a.shape)
    if is_numeric(a):
        print('max:', a.max(axis=0))
        print('min:', a.min(axis=0))


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
