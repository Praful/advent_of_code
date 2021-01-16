import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/5

const bool DEBUG = false;

Object part1(String header, List input) {
  printHeader(header);
  print(input);
  return Computer(input).run(0);
}

Object part2(String header, List input) {
  printHeader(header);
}

void main(List<String> arguments) {
  // List testInput = FileUtils.asLines('../data/day05-test.txt');
  List mainInput = FileUtils.asString('../data/day05.txt')
      .split(',')
      .map((v) => v.toInt())
      .toList();

  assertEqual(
      part1('05 test part 1', [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]),
      3500);
  assertEqual(part1('05 test part 1a', [1, 0, 0, 0, 99]),
      2); // => 2,0,0,0,99 (1 + 1 = 2).
  assertEqual(part1('05 test part 1b', [2, 3, 0, 3, 99]),
      2); // => 2,3,0,6,99 (3 * 2 = 6).
  assertEqual(part1('05 test part 1c', [2, 4, 4, 5, 99, 0]),
      2); // => 2,4,4,5,99,9801 (99 * 99 = 9801).
  assertEqual(part1('05 test part 1', [1, 1, 1, 4, 99, 5, 6, 0, 99]),
      30); // => 30,1,1,4,2,5,6,0,99.

  //Answer:
  // assertEqual(part1('05 test part 1', testInput), 1);
  //Answer:
  // assertEqual(part2('05 test part 2', testInput), 1);

  //Answer:13818007
  print(part1('05 part 1', mainInput));
  //Answer:
  // print(part2('05 part 2', mainInput));
}
