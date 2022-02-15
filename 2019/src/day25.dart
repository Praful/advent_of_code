import '../../shared/dart/src/utils.dart';
// import 'dart:math';
import './intcode_computer.dart';
// import '../../shared/dart/src/grid.dart';
import 'dart:io';

/// Puzzle description: https://adventofcode.com/2019/day/25

// This program doesn't solve day 25. Instead you play the game interactively,
// which is what I did to find the answer. I wrote it to see what was going on
// and the answer popped out. I decided to call it a day (or year) and move on
// to another AoC year.

const bool DEBUG = false;
const String DELIM = ',';
const int LF = 10;
const String CHECKPOINT = 'Security Checkpoint';
const List<String> AVOID_ITEMS = [
  'giant electromagnet',
  'escape pod',
  'molten lava',
  'photons',
  'infinite loop'
];
const List<String> DIRECTION = ['north', 'south', 'east', 'west'];
const Map<String, String> DIR_OPPOSITE = {
  'north': 'south',
  'south': 'north',
  'east': 'west',
  'west': 'east'
};

var inputCommands = <int>[];

class Room {
  static Set inventory = <String>{};

  List<String> directions = [];
  List items = <String>[];
  String name = '';
  bool isCheckpoint = false;
  Room(List<String> contents) {
    for (var c in contents) {
      if (c.startsWith('- ')) {
        var s = c.substring(2);
        if (DIRECTION.contains(s)) {
          directions.add(s);
        } else if (!AVOID_ITEMS.contains(s)) {
          items.add(s);
        }
      } else if (c.startsWith('==')) {
        name = c.substring(3);
        if (c.contains(CHECKPOINT)) isCheckpoint = true;
      }
    }
  }
  @override
  String toString() {
    return 'Name: $name\nDirections: $directions\nItems: $items\nCheckpoint: $isCheckpoint\nInventory: $inventory';
  }
}

String asciiCodeToText(List<int> output) =>
    output.isNotEmpty ? String.fromCharCode(output.first) : '';

void traverse(program) {
  var inputCommands = [LF];
  var robot = Computer(program, () => inputCommands.removeAt(0));
  var accOutput = '';
  var cmdHistory = <String>[];

  while (!robot.halted) {
    robot.run([], true);
    var output = robot.output(true);
    if (output.isNotEmpty) {
      var char = asciiCodeToText(output);

      if (output.first == LF) {
        if (accOutput.isNotEmpty) {
          cmdHistory.add(accOutput);
          print('$accOutput');
        }
        if (accOutput == 'Command?') {
          var command = stdin.readLineSync();
          if (command != null && command.isEmpty) {
            inputCommands = [LF];
          } else {
            inputCommands = [...command!.codeUnits, LF];
          }
          if (!command.contains('take ')) cmdHistory.clear();
        }
        accOutput = '';
      } else {
        accOutput += char;
      }
    }
  }
}

Object part1(String header, List input) {
  printHeader(header);
  traverse(input);

  return 0;
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day25.txt', DELIM);
  printAndAssert(part1('25 part 1', mainInput)); // 1077936448
}
