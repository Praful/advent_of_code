import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;
const String PC = 'program counter';
const String ACC = 'accumulator';

final List<String> TEST_INPUT = File('./data/day08-test.txt').readAsLinesSync();
// final String TEST_INPUT2 = File('./data/day07b-test.txt').readAsStringSync();

final List<String> MAIN_INPUT = File('./data/day08.txt').readAsLinesSync();

Map<String, int> blankAnswer() => <String, int>{ACC: 0, PC: 0};

Map<String, int> runCode(List input) {
  var acc = 0, pc = 0, visited = <int>{}, result = blankAnswer();
  var re =
      RegExp(r'^(?<instruction>(nop|acc|jmp))\s(?<operator>.)(?<value>\d+)$');

  while (!visited.contains(pc) && pc < input.length) {
    visited.add(pc);
    var match = re.firstMatch(input[pc]);
    var instruction = match.namedGroup('instruction');
    var op = match.namedGroup('operator');
    var value = int.parse(match.namedGroup('value'));
    switch (instruction) {
      case 'nop':
        pc++;
        break;
      case 'acc':
        acc += ((op == '+' ? 1 : -1) * value);
        pc++;
        break;
      case 'jmp':
        pc += ((op == '+' ? 1 : -1) * value);
        break;
      default:
        print('invalid instruction: $instruction');
    }
  }
  result[ACC] = acc;
  result[PC] = pc;
  return result;
}

Map<String, int> runScenarios(input) {
  var result = blankAnswer();

  Map<String, int> tryNewInput(i, from, to) {
    var newInput = List.from(input);
    newInput[i] = input[i].replaceFirst(from, to);
    return runCode(newInput);
  }

  bool foundSolution() => (result[PC] >= input.length);

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
