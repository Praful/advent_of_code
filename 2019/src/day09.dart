import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import 'package:collection/collection.dart';

/// Puzzle description: https://adventofcode.com/2019/day/9

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

List part1(String header, List<int> program, [List<int> input]) {
  printHeader(header);
  var c = Computer(program);
  c.run(input);
  print('output: ${c.output()}');
  return c.output();
}

int part2(String header, List<int> program, [List<int> input]) {
  printHeader(header);
  var c = Computer(program);
  c.run(input);
  print('output: ${c.output()}');
  return c.output().last;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asInt('../data/day09-test.txt', ',');
  List testInputb = FileUtils.asInt('../data/day09b-test.txt', ',');
  List testInputc = FileUtils.asInt('../data/day09c-test.txt', ',');
  List mainInput = FileUtils.asInt('../data/day09.txt', ',');

  assertEqual(
      DeepCollectionEquality()
          .equals(part1('09 test part 1', testInput), testInput),
      true);
  assertEqual(part1('09 test part 1b', testInputb).last.toString().length, 16);
  assertEqual(part1('09 test part 1c', testInputc).last, 1125899906842624);

  printAndAssert(part1('09 part 1', mainInput, [1]).last, 2399197539);
  printAndAssert(part2('09 part 2', mainInput, [2]), 35106);
}
