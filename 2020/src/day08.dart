import 'dart:io';
import '../utils.dart';

const bool DEBUG = false;

final List<String> TEST_INPUT = File('./data/day08-test.txt').readAsLinesSync();
final List<String> MAIN_INPUT = File('./data/day08.txt').readAsLinesSync();

class Computer {
  final List input;
  int _pc = 0;
  int _acc = 0;
  bool _hasRun = false;

  Computer(this.input);

  bool wasNormallyTerminated() => (!_hasRun
      ? throw 'Program has not run. Call run() first with input.'
      : _pc == input.length);

  int get accumulator {
    return _acc;
  }

  static final INSTRUCTION_REGEX = RegExp(
      r'^(?<instruction>(nop|acc|jmp))\s(?<operator>(\+|\-))(?<value>\d+)$');

  int run() {
    assert(input != null);

    var visited = <int>{};

    int increment(start, op, value) =>
        (start += ((op == '+' ? 1 : -1) * value));

    while (!visited.contains(_pc) && _pc < input.length) {
      visited.add(_pc);
      var match = INSTRUCTION_REGEX.firstMatch(input[_pc]);
      var instruction = match.namedGroup('instruction');
      var op = match.namedGroup('operator');
      var value = int.parse(match.namedGroup('value'));
      switch (instruction) {
        case 'nop':
          _pc++;
          break;
        case 'acc':
          _acc = increment(_acc, op, value);
          _pc++;
          break;
        case 'jmp':
          _pc = increment(_pc, op, value);
          break;
        default:
          print('invalid instruction: $instruction');
      }
    }
    _hasRun = true;
    return accumulator;
  }
}

//Use brute force method to try different inputs, changing one nop/jmp
//at a time until Computer run finishes without looping.
int runScenarios(input) {
  Computer tryNewInput(i, from, to) {
    var newInput = List.from(input);
    newInput[i] = input[i].replaceFirst(from, to);
    var computer = Computer(newInput);
    computer.run();
    return computer;
  }

  var computer = Computer(<String>[]);

  for (var i = 0; i < input.length; i++) {
    if (input[i].startsWith('nop')) {
      computer = tryNewInput(i, 'nop', 'jmp');
    } else if (input[i].startsWith('jmp')) {
      computer = tryNewInput(i, 'jmp', 'nop');
    }
    if (computer.wasNormallyTerminated()) break;
  }
  return computer.accumulator;
}

void test() {
  printHeader('7a test');
  //Answer: 5
  print(Computer(TEST_INPUT).run());
  //Answer: 8
  print(runScenarios(TEST_INPUT));
}

void part1() {
  printHeader('8a');
  //Answer: 1451
  print(Computer(MAIN_INPUT).run());
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
