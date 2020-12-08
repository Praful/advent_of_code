import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

final List<String> TEST_INPUT = File('./data/day08-test.txt').readAsLinesSync();
// final String TEST_INPUT2 = File('./data/day07b-test.txt').readAsStringSync();

final List<String> MAIN_INPUT = File('./data/day08.txt').readAsLinesSync();

Map<String, int> runCode(List input) {
  var acc = 0, pos = 0, visited = <int>{};
  var re =
      RegExp(r'^(?<instruction>(nop|acc|jmp))\s(?<operator>.)(?<value>\d+)$');
  while (!visited.contains(pos) && pos < input.length) {
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
  return {'acc': acc, 'pos': pos};
}

Map<String, int> runScenarios(input) {
  var result = {'acc': 0, 'pos': 0};

  Map<String, int> tryNewInput(i, from, to) {
    var newInput = List.from(input);
    newInput[i] = input[i].replaceFirst(from, to);
    return runCode(newInput);
  }

  bool foundSolution() => (result['pos'] >= input.length);

  for (var i = 0; i < input.length; i++) {
    if (input[i].startsWith('nop')) {
      result = tryNewInput(i, 'nop', 'jmp');
    } else if (input[i].startsWith('jmp')) {
      result = tryNewInput(i, 'jmp', 'nop');
    }
    if (foundSolution()) break;
  }
  return result;
}

void test() {
  printHeader('7a test');
  //Answer: 5
  print(runCode(TEST_INPUT));
  //Answer: 8
  print(runScenarios(TEST_INPUT));
}

void part1() {
  printHeader('8a');
  //Answer: 1451
  print(runCode(MAIN_INPUT));
}

void part2() {
  printHeader('8b');
  //Answer: 1160
  print(runScenarios(MAIN_INPUT));
}

//test cloning of List
void test2() {
  var a = ['first', 'second', 'third'];
  print(a);
  // var b = [...a]; //this works too
  var b = List.from(a);
  print(b);
  a[0] = 'ten';
  print(a);
  print(b);
}

void main(List<String> arguments) {
  test();
  // test2();
  part1();
  part2();
}
