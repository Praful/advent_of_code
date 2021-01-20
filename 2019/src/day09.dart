import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/9

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

Object part1(String header, List<int> program, [List<int> input]) {
  printHeader(header);
  var c = Computer(program);
  c.run(input);
  return c.output;
}

Object part2(String header, List<int> program, [List<int> input]) {
  printHeader(header);
  var c = Computer(program);
  c.run(input);
  return c.output;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asInt('../data/day09-test.txt', ',');
  List testInputb = FileUtils.asInt('../data/day09b-test.txt', ',');
  List testInputc = FileUtils.asInt('../data/day09c-test.txt', ',');
  List mainInput = FileUtils.asInt('../data/day09.txt', ',');

  //Answer:
  assertEqual(part1('09 test part 1', testInput), 99);
  assertEqual(part1('09 test part 1b', testInputb).toString().length, 16);
  assertEqual(part1('09 test part 1c', testInputc), 1125899906842624);

  printAndAssert(part1('09 part 1', mainInput, [1]), 2399197539);
  printAndAssert(part2('09 part 2', mainInput, [2]), 35106);
}
