import re
import functools
from collections import *
# from collections import namedtuple
from pprint import pprint
from enum import Enum

# These are a collection of tips I've picked up and syntax reminders.

# some these are from Raymond Hettinger's talk:
# https://www.youtube.com/watch?v=OSGv2VnC0go

# regular expressions
# if multiple matches on line, use re.findall() then match[0][0], match[0][1], etc
l = ['Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
     'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
     'Valve CC has flow rate=2; tunnels lead to valves DD, BB']
for s in l:
    match = re.search(
        r'^Valve (..) has flow rate=(\d*).* valves? (.*)$', s)
    if match:
        [print(match.group(i)) for i in range(4)]


# loops
colors = ['red', 'green', 'blue', 'yellow']
names = ['alpha', 'beta', 'gamma', 'delta']

# reverse list
for color in reversed(colors):
    print(color)

# Backwards sorted order
for color in sorted(colors, reverse=True):
    print(color)

# get index and value
for i, color in enumerate(colors):
    print(f'{i} -> {color}')


# iterate two lists together
for color, greek in zip(colors, names):
    print(f'{color} - {greek}')

# list comprehension
a= [1,2,3,4]
total = sum(n for n in a)
print(a, total)

# custom sort, instead of using a sort function
print(sorted(colors, key=len))

# loop until a certain (sentinel) value occurs
# iter takes two arguments:
# 1. function you call repeatedly
# 2. sentinel value (exit condition)
# partial creates a new function with a simplified signature; in this case
# iter requires a function with no args

# blocks = []
# for block in iter(functools.partial(f.read, 32), ''):
# blocks.append(block)


# for/else loop: else called if loop ended early, in this case with break
def find(seq, target):
    for i, value in enumerate(seq):
        if value == target:
            break
    else:
        return -1
    return i


# dictionary from pairs
print(dict(zip(names, colors)))


# group by length
d = defaultdict(list)
for name in names:
    key = len(name)
    d[key].append(name)
print(d)


# improve clarity to function calls by using keyword arguments
# twitter_search('@obama', retweets=False, numtweets=20, popular=True)

# clearer to use names tuples; can be used to return tuples
# can also have namedtuple("Point", ["x", y"])
Point = namedtuple("Point", "x y")
print(Point(2, 4))

# unpack sequence
n = 'a', 'b', 'c'
first, second, third = n
print(first, second, third)


# updating multiple state variables instead of using temp variable
def fibonacci(n):
    x, y = 0, 1
    for i in range(n):
        # print(x)
        x, y = y, x + y
    return x


print(fibonacci(7))

# for example of data classes see ../../2023/src/day03.py

# concatenating strings
# use join() instead of looping and doing s += ', ' + name
print(', '.join(names))

# updating sequences
# if code has name.pop(0) or name.insert(0, 'xyz), use deque() for faster code:
names2 = deque(names)
print(names2.popleft())
names2.appendleft(('epsilon'))
print(names2)

# for pure functions (same output for same input), can use decorators to cache values:
# @lru_cache
# def lookup(x,y):
#   return complex_calculation(x, y)


# match/switch statement
# see https://peps.python.org/pep-0636/
s = 'abcd'
match s[0]:
    case 'a': print('a matched')
    case 'b': print('b matched')
    # Other cases
    case _:
        print(f"Other: {s}")


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


c = Color.GREEN
match c:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
