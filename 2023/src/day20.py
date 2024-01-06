from collections import defaultdict
from collections import namedtuple
import os
import sys
import queue
from pprint import pprint
from enum import Enum

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/20

# For part 2, this uses a similar approach to day 8. The assumption, which
# turns out to be true, is that the modules inputting to the rx module each
# have their own repeating cycle. LCM is then used once we've found the cycle
# length.

Module = namedtuple('Module', ['id', 'type', 'destination', 'state'])


class Type(Enum):
    FLIP_FLOP = '%'
    CONJUNCTION = '&'


class Pulse(Enum):
    HIGH = True
    LOW = False

    @classmethod
    def flip(cls, pulse): return cls(not pulse.value)


def read_input(input_file):
    modules = {}
    conj_inputs = defaultdict(dict)

    for l in read_file_str(input_file, True):
        s = l.split(' -> ')
        destination = s[1].split(', ')
        if l.startswith('broadcaster'):
            modules[s[0]] = Module(
                'broadcaster', 'broadcaster', destination, Pulse.LOW)
        else:
            name = s[0][1:]
            type = Type(s[0][0])
            modules[name] = Module(name, type, destination, Pulse.LOW)
            for d in destination:
                conj_inputs[d][name] = Pulse.LOW

    return modules, conj_inputs


def solve(input, part1=True):
    def tr(x):
        if x:
            return '-high->'
        else:
            return '-low->'

    def send_pulses(receiver, pulse):
        for dest in receiver.destination:
            q.put((receiver.id, dest, pulse))

    #  pprint(input)
    modules, conj_inputs = input
    broadcaster = modules['broadcaster']

    q = queue.SimpleQueue()
    pulse_count = {Pulse.HIGH: 0, Pulse.LOW: 0}
    result1 = result2 = None

    # part 2 vars
    first_cycle = {}
    second_cycle = {}
    rx_sender = conj_inputs['rx']

    pushes = 0
    while True:
        pushes += 1
        if part1 and pushes > 1000:
            result1 = pulse_count[Pulse.HIGH] * pulse_count[Pulse.LOW]
            break

        pulse_count[Pulse.LOW] += 1  # button press
        send_pulses(broadcaster, Pulse.LOW)

        while not q.empty():
            sender, receiver_id, pulse = q.get()
            #  print(sender, tr(pulse), receiver_id)
            pulse_count[pulse] += 1

            if receiver_id not in modules:
                continue

            receiver = modules[receiver_id]

            match receiver.type:
                case Type.FLIP_FLOP:
                    if pulse == Pulse.LOW:  # high pulses are ignored
                        new_pulse = Pulse.flip(receiver.state)
                        modules[receiver_id] = receiver._replace(
                            state=new_pulse)
                        send_pulses(receiver, new_pulse)

                case Type.CONJUNCTION:
                    inputs = conj_inputs[receiver.id]
                    inputs[sender] = pulse

                    if not part1 and receiver.id in rx_sender and pulse == Pulse.HIGH:
                        #  print(t, receiver_id, inputs)
                        if sender not in first_cycle:
                            first_cycle[sender] = pushes
                        elif sender not in second_cycle:
                            second_cycle[sender] = pushes

                        if len(second_cycle) == len(inputs):
                            result2 = lcm(second_cycle[s] - first_cycle[s]
                                          for s in second_cycle.keys())
                            break

                    new_pulse = Pulse(
                        not all(r == Pulse.HIGH for r in inputs.values()))
                    send_pulses(receiver, new_pulse)

                case _:
                    raise Exception(f'Unknown type {receiver.type}')

        if result2 is not None:
            break

    return result1, result2


def main():
    input = read_input("../data/day20.txt")
    test_input1 = read_input("../data/day20-test-1.txt")
    test_input2 = read_input("../data/day20-test-2.txt")

    assert (res := solve(test_input1))[0] == 32000000, f'Actual: {res}'
    assert (res := solve(test_input2))[0] == 11687500, f'Actual: {res}'
    print(f'Part 1 {solve(input)[0]}')  # 684125385  (16195 x 42243)

    # reset input
    input = read_input("../data/day20.txt")
    print(f'Part 2 {solve(input, False)[1]}')  # 225872806380073


if __name__ == '__main__':
    main()
