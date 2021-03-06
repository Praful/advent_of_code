import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/7

const bool DEBUG = false;


int run1(program, input) {
  var c = Computer(program);
  c.run(input);
  // print(c.output);
  return c.output().last;
}

Object part1(String header, List input) {
  printHeader(header);
  var perms = Permutations(5, range(0, 5).toList());
  return perms().map((phase) {
    var signal = 0;
    for (var i in range(0, 5)) {
      signal = run1(input, [phase[i], signal]);
    }
    return signal;
  }).max;
}

int run2(Computer amp, int phase, int signal) {
  return amp.run([phase, signal], true).last;
  // return amp.output;
}

Object part2(String header, List<int> input) {
  printHeader(header);
  var perms = Permutations(5, range(5, 10).toList());

  return perms().map((phase) {
    var amps = range(0, 5).map((_) => Computer(input)).toList();
    var signal = 0; //first call to amp0 takes 0 as signal
    while (!amps[4].halted) {
      for (var i in range(0, 5)) {
        signal = run2(amps[i], phase[i], signal);
      }
    }
    return amps[4].output().last;
  }).max;
}

void main(List<String> arguments) {
  var testInput = FileUtils.asInt('../data/day07-test.txt', ',');
  var testInput1b = FileUtils.asInt('../data/day07b-test.txt', ',');
  var testInput1c = FileUtils.asInt('../data/day07c-test.txt', ',');
  var testInput2a = FileUtils.asInt('../data/day07d-test.txt', ',');
  var testInput2b = FileUtils.asInt('../data/day07e-test.txt', ',');
  var mainInput = FileUtils.asInt('../data/day07.txt', ',');

  assertEqual(part1('07 test part 1', testInput), 43210);
  assertEqual(part1('07 test part 1b', testInput1b), 54321);
  assertEqual(part1('07 test part 1c', testInput1c), 65210);

  assertEqual(part2('07 test part 2d', testInput2a), 139629729);
  assertEqual(part2('07 test part 2e', testInput2b), 18216);

  printAndAssert(part1('07 part 1', mainInput), 13848);
  printAndAssert(part2('07 part 2', mainInput), 12932154);
}
