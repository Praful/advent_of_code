import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

final List TEST_INPUT = File('./data/day08-test.txt').readAsLinesSync();
// final String TEST_INPUT2 = File('./data/day07b-test.txt').readAsStringSync();

final List MAIN_INPUT = File('./data/day08.txt').readAsLinesSync();

int runCode(input) {
  var acc = 0, pos = 0, visited = <int>{};
  var re =
      RegExp(r'^(?<instruction>(nop|acc|jmp))\s(?<operator>.)(?<value>\d+)$');
  while (!visited.contains(pos)) {
    visited.add(pos);
    var match = re.firstMatch(input[pos]);
    var instruction = match.namedGroup('instruction');
    var op = match.namedGroup('operator');
    var value = int.parse(match.namedGroup('value'));
    // print('------- $instruction, $op, $value, $acc, $pos');
    switch (instruction) {
      case 'nop':
        pos++;
        break;
      case 'acc':
        acc += ((op == '+' ? 1 : -1) * value);
        pos++;
        break;
      case 'jmp':
        pos += ((op == '+' ? 1 : -1) * value);
        break;
      default:
        print('invalid instruction: $instruction');
    }
    // print('$acc, $pos');
  }
  return acc;
}

void test() {
  printHeader('7a test');
  //Answer: 5
  print(runCode(TEST_INPUT));
}

void part1() {
  //Answer: 1451
  printHeader('8a');
  print(runCode(MAIN_INPUT));
}

void part2() {
  printHeader('8b');
}

void main(List<String> arguments) {
  test();
  part1();
  part2();
}
