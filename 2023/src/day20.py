from collections import defaultdict
from collections import namedtuple
import os
import sys
import queue
from pprint import pprint

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/20


# state: True: on or high pulse, False: off or low pulse
Module = namedtuple('Module', ['id', 'type', 'destination', 'state'])

HIGH = True
LOW = False


def read_input(input_file):
    modules = {}
    conj_inputs = defaultdict(dict)

    for l in read_file_str(input_file, True):
        s = l.split(' -> ')
        destination = s[1].split(', ')
        if l.startswith('broadcaster'):
            modules[s[0]] = Module(
                'broadcaster', 'broadcaster', destination, LOW)
        else:
            name = s[0][1:]
            type = s[0][0]
            modules[name] = Module(name, type, destination, LOW)
            for d in destination:
                conj_inputs[d][name] = LOW

    return modules, conj_inputs


def solve(input, part1=True):
    def tr(x):
        if x:
            return '-high->'
        else:
            return '-low->'

    def update_queue(receiver, pulse):
        for d in receiver.destination:
            q.put((receiver.id, d, pulse))

    #  pprint(input)
    modules, conj_inputs = input
    high = low = 0
    broadcaster = modules['broadcaster']

    first_cycle = {}
    second_cycle = {}
    result1 = result2 = None
    rx_sender = conj_inputs['rx']
    q = queue.SimpleQueue()
    t = 0

    while True:
        t += 1
        if part1 and t > 1000:
            result1 = low * high
            break

        low += 1  # button press
        for receiver_id in broadcaster.destination:
            q.put((broadcaster.id, receiver_id, LOW))

        while not q.empty():
            sender, receiver_id, pulse = q.get()
            #  print(sender, tr(pulse), receiver_id)
            if pulse:
                high += 1
            else:
                low += 1

            if receiver_id not in modules:
                continue

            receiver = modules[receiver_id]

            if receiver.type == '%':
                if pulse == LOW:  # high pulses are ignored
                    new_pulse = not receiver.state
                    modules[receiver_id] = receiver._replace(state=new_pulse)
                    update_queue(receiver, new_pulse)

            elif receiver.type == '&':
                inputs = conj_inputs[receiver.id]
                inputs[sender] = pulse

                if not part1 and receiver.id in rx_sender and pulse == HIGH:
                    #  print(t, receiver_id, inputs)
                    if sender not in first_cycle:
                        first_cycle[sender] = t
                    elif sender not in second_cycle:
                        second_cycle[sender] = t

                    if len(second_cycle) == len(inputs):
                        result2 = lcm(second_cycle[s] - first_cycle[s]
                                      for s in second_cycle.keys())
                        break

                new_pulse = not all(r == HIGH for r in inputs.values())
                update_queue(receiver, new_pulse)

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

    print(f'Part 2 {solve(input, False)[1]}')  # 225872806380073


if __name__ == '__main__':
    main()
