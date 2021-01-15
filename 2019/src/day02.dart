import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';

/// Puzzle description: https://adventofcode.com/2019/day/2

const bool DEBUG = false;

class Computer {
  static const OPCODE_ADD = 1;
  static const OPCODE_MULTIPY = 2;
  static const OPCODE_HALT = 99;
  static const OP_LENGTH = 4;

  List<int> program;
  Computer(data) {
    program = List.from(data);
  }

  int run(returnAddress) {
    var pc = 0; //program counter
    var value = 0;
    while (value != OPCODE_HALT) {
      value = program[pc];
      var operand1, operand2, storeAddress;
      if (value != OPCODE_HALT) {
        operand1 = program[program[pc + 1]];
        operand2 = program[program[pc + 2]];
        storeAddress = program[pc + 3];
      }
      switch (value) {
        case OPCODE_ADD:
          program[storeAddress] = operand1 + operand2;
          break;
        case OPCODE_MULTIPY:
          program[storeAddress] = operand1 * operand2;
          break;
        default:
        //do nothing
      }
      pc += OP_LENGTH;
    }
    // print(input);
    return program[returnAddress];
  }
}

Object part1(String header, List input) {
  printHeader(header);
  return Computer(input).run(0);
}

List initProgram(program, noun, verb) {
  var result = List.from(program);
  result[1] = noun;
  result[2] = verb;
  return result;
}

//more declarative alternative for part 2
Object part2a(String header, List input, int targetOutput) {
  printHeader(header);

  int runProgram(noun, verb) => Computer(initProgram(input, noun, verb)).run(0);

  var nounVerb = Amalgams(2, range(0, 100).toList())()
      .skipWhile((nv) => (runProgram(nv[0], nv[1]) != targetOutput))
      .first;

  return (100 * nounVerb[0]) + nounVerb[1];
}

Object part2(String header, List input, int targetOutput) {
  printHeader(header);

  var combos = Amalgams(2, range(0, 100).toList());
  for (var nounVerb in combos()) {
    var newInput = List.from(input);
    newInput[1] = nounVerb[0];
    newInput[2] = nounVerb[1];
    var c = Computer(newInput);
    if (c.run(0) == targetOutput) {
      return (100 * nounVerb[0]) + nounVerb[1];
    }
  }
  return null;
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asString('../data/day02.txt')
      .split(',')
      .map((v) => v.toInt())
      .toList();

  assertEqual(
      part1('02 test part 1', [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]),
      3500);
  assertEqual(part1('02 test part 1a', [1, 0, 0, 0, 99]),
      2); // => 2,0,0,0,99 (1 + 1 = 2).
  assertEqual(part1('02 test part 1b', [2, 3, 0, 3, 99]),
      2); // => 2,3,0,6,99 (3 * 2 = 6).
  assertEqual(part1('02 test part 1c', [2, 4, 4, 5, 99, 0]),
      2); // => 2,4,4,5,99,9801 (99 * 99 = 9801).
  assertEqual(part1('02 test part 1', [1, 1, 1, 4, 99, 5, 6, 0, 99]),
      30); // => 30,1,1,4,2,5,6,0,99.

  //Answer: 4023471
  print(part1('02 part 1', initProgram(mainInput, 12, 2)));

  //Answer: 8051
  print(part2a('02 part 2', mainInput, 19690720));
}
