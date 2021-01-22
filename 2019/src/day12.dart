import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/12

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
  List testInput = FileUtils.asLines('../data/day12-test.txt');
  List mainInput = FileUtils.asLines('../data/day12.txt');

  //Answer:
  assertEqual(part1('12 test part 1', testInput), 1);
  //Answer:
  // assertEqual(part2('12 test part 2', testInput), 1);

  //Answer:
  // printAndAssert(part1('12 part 1', mainInput));
  //Answer:
  // printAndAssert(part2('12 part 2', mainInput));
}
