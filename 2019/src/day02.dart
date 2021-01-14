import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

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

Object runPart1(String name, List input) {
  printHeader(name);
  return Computer(input).run(0);
}

List initProgram(program, noun, verb) {
  var result = List.from(program);
  result[1] = noun;
  result[2] = verb;
  return result;
}

//more declarative alternative for part 2
Object runPart2a(String name, List input, int targetOutput) {
  printHeader(name);

  int runProgram(noun, verb) => Computer(initProgram(input, noun, verb)).run(0);

  var nounVerb = Amalgams(2, range(0, 100).toList())()
      .skipWhile((nv) => (runProgram(nv[0], nv[1]) != targetOutput))
      .first;

  return (100 * nounVerb[0]) + nounVerb[1];
}

Object runPart2(String name, List input, int targetOutput) {
  printHeader(name);

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
}

void main(List<String> arguments) {
  MAIN_INPUT = FileUtils.asString('../data/day02.txt')
      .split(',')
      .map((v) => v.toInt())
      .toList();

  //Answer:
  print(runPart1('02 test part 1', [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]));
  print(runPart1(
      '02 test part 1', [1, 0, 0, 0, 99])); // => 2,0,0,0,99 (1 + 1 = 2).
  print(runPart1(
      '02 test part 1', [2, 3, 0, 3, 99])); // => 2,3,0,6,99 (3 * 2 = 6).
  print(runPart1('02 test part 1',
      [2, 4, 4, 5, 99, 0])); // => 2,4,4,5,99,9801 (99 * 99 = 9801).
  print(runPart1('02 test part 1',
      [1, 1, 1, 4, 99, 5, 6, 0, 99])); // => 30,1,1,4,2,5,6,0,99.

  //Answer:
  // print(runPart2('02 test part 2', TEST_INPUT));

  //Answer: 4023471
  print(runPart1('02 part 1', initProgram(MAIN_INPUT, 12, 2)));

  //Answer: 8051
  print(runPart2a('02 part 2', MAIN_INPUT, 19690720));
}
