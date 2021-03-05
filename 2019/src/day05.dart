import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/5

const bool DEBUG = false;

List run(List<int> program, int returnAddress, input) {
  var c = Computer(program);
  c.run(input);
  return [c.memory[returnAddress], c.output().isEmpty ? null : c.output().last];
}

int part1Day2(String header, List<int> program) {
  printHeader(header);
  var writeInput = 1;
  var returnAddress = 0;
  return run(program, returnAddress, [writeInput])[0];
}

int general(String header, List<int> program, int initValue) {
  printHeader(header);
  var returnAddress = 0;
  return run(program, returnAddress, [initValue])[1];
}

int part1(String header, List<int> program, int initValue) {
  return general(header, program, initValue);
}

int part2(String header, List<int> program, int initValue) {
  return general(header, program, initValue);
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asString('../data/day05.txt')
      .split(',')
      .map((v) => v.toInt())
      .toList();

  //Part 1 tests from day 2.
  assertEqual(
      part1Day2('05 test part 1', [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]),
      3500);
  assertEqual(part1Day2('05 test part 1a', [1, 0, 0, 0, 99]),
      2); // => 2,0,0,0,99 (1 + 1 = 2).
  assertEqual(part1Day2('05 test part 1b', [2, 3, 0, 3, 99]),
      2); // => 2,3,0,6,99 (3 * 2 = 6).
  assertEqual(part1Day2('05 test part 1c', [2, 4, 4, 5, 99, 0]),
      2); // => 2,4,4,5,99,9801 (99 * 99 = 9801).
  assertEqual(part1Day2('05 test part 1d', [1, 1, 1, 4, 99, 5, 6, 0, 99]),
      30); // => 30,1,1,4,2,5,6,0,99.

  assertEqual(
      part2('05 test part 2a', [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8), 1); //1
  assertEqual(
      part2('05 test part 2b', [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7), 0); //0
  assertEqual(
      part2('05 test part 2c', [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 9], 7), 1); //1
  assertEqual(
      part2('05 test part 2d', [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9), 0); //0
  assertEqual(
      part2('05 test part 2e', [3, 3, 1108, -1, 8, 3, 4, 3, 99], 8), 1); //1
  assertEqual(
      part2('05 test part 2f', [3, 3, 1108, -1, 8, 3, 4, 3, 99], 9), 0); //0
  assertEqual(
      part2('05 test part 2g', [3, 3, 1107, -1, 8, 3, 4, 3, 99], 7), 1); //1
  assertEqual(
      part2('05 test part 2g', [3, 3, 1107, -1, 8, 3, 4, 3, 99], 9), 0); //0

  //Answer:13818007
  printAndAssert(part1('05 part 1', mainInput, 1), 13818007);
  //Answer: 3176266
  printAndAssert(part2('05 part 2', mainInput, 5), 3176266);
}
