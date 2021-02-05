import 'dart:io';
import 'dart:math';
import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/17

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

int calibrateCameras(List<int> input) {
  // var AsciiCodeToString = {}
  //   ..[94] = '^'
  //   ..[62] = '>'
  //   ..[60] = '<'
  //   ..[118] = 'v'
  //   ..[35] = '#'
  //   ..[46] = '.'
  //   ..[10] = '\n';

  var robot = Computer(input);
  var view = '';
  var x = 0, y = 0;
  var scaffold = <Point, int>{};
  while (!robot.halted) {
    robot.run([], true);
    var output = robot.output(true);
    if (output.isNotEmpty) {
      var char = String.fromCharCode(output.first);
      view += char;
      if (output.first == 10) {
        x = 0;
        y++;
      } else if (char == '#') {
        scaffold[Point(x++, y)] = output.first;
      } else {
        x++;
      }
    }
  }
  print(view);
  // print(scaffold);
  return calcAlignmentParameters(scaffold);
}

enum Direction { up, down, left, right }

final adjacentPoints = {}
  ..[Direction.right] = Point(1, 0)
  ..[Direction.left] = Point(-1, 0)
  ..[Direction.up] = Point(0, 1)
  ..[Direction.down] = Point(0, -1);

bool isIntersection(Map scaffold, Point p) =>
    Direction.values.every((d) => scaffold.containsKey(p + adjacentPoints[d]));

int calcAlignmentParameters(Map scaffold) => scaffold.keys
    .fold(0, (acc, p) => acc + (isIntersection(scaffold, p) ? p.x * p.y : 0));

Object part1(String header, List input) {
  printHeader(header);
  return calibrateCameras(input);
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

void main(List<String> arguments) {
  // List testInput = FileUtils.asLines('../data/day17-test.txt');
  List mainInput = FileUtils.asInt('../data/day17.txt', ',');

  // assertEqual(part1('17 test part 1', testInput), 1);
  // assertEqual(part2('17 test part 2', testInput), 1);

  printAndAssert(part1('17 part 1', mainInput), 2788);
  // printAndAssert(part2('17 part 2', mainInput));
}
