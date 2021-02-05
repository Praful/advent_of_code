import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

Object part1(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/dayXX-test.txt');
  List mainInput = FileUtils.asLines('../data/dayXX.txt');

  assertEqual(part1('XX test part 1', testInput), 1);
  // assertEqual(part2('XX test part 2', testInput), 1);

  // printAndAssert(part1('XX part 1', mainInput));
  // printAndAssert(part2('XX part 2', mainInput));
}
