import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

Object part1(String header, List input) {
  printHeader(header);
}

Object part2(String header, List input) {
  printHeader(header);
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/dayXX-test.txt');
  List mainInput = FileUtils.asLines('../data/dayXX.txt');

  //Answer:
  assertEqual(part1('XX test part 1', testInput), 1);
  //Answer:
  // assertEqual(part2('XX test part 2', testInput), 1);

  //Answer:
  // print(part1('XX part 1', mainInput));
  //Answer:
  // print(part2('XX part 2', mainInput));
}
