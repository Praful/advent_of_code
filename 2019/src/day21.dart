import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/21

const bool DEBUG = false;
const DELIM = ',';
const LF = 10;
const HULL = '#';
const SPACE = '.';
const SPRINGDROID = '@';
const RUN_COMMAND = 'WALK';

String asciiCodeToText(List<int> output) =>
    output.isNotEmpty ? String.fromCharCode(output.first) : '';

Object surveyHull(program, command) {
  var response = '';
  var result = 0;
  var output;

  var inputCommand = [...command.codeUnits];
  // print(inputCommand);
  var robot = Computer(program, () => inputCommand.removeAt(0));
  while (!robot.halted) {
    robot.run([], true);
    output = robot.output(true);
    if (output.isNotEmpty) {
      if (output.first == LF) {
        print(response);
        response = '';
      } else if (output.first < 255) {
        response += asciiCodeToText(output);
      }
      //The last output is the hull damage
      result = output.first;
    }
  }
  return result;
}

Object part1(String header, List input) {
  printHeader(header);
  var command1 = 'NOT D J\nWALK\n';
  var command2 = '''
NOT C J
NOT A T
OR T J
AND D J
WALK
''';
  return surveyHull(input, command2);
}

Object part2(String header, List input) {
  printHeader(header);
  var command1 = 'NOT D J\nRUN\n';
  var command4 = '''
NOT C J
NOT B T
OR T J
NOT A T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
RUN
''';

  var command2 = '''
NOT C J
NOT A T
OR T J
AND D J
RUN
''';
  return surveyHull(input, command4);
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day21.txt', DELIM);

  printAndAssert(part1('21 part 1', mainInput), 19347868);
  printAndAssert(part2('21 part 2', mainInput), 1142479667);
}
