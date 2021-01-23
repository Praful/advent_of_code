import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

enum Tile { empty, wall, block, paddle, ball }
const X_INDEX = 0;
const Y_INDEX = 1;
const TILE_ID_INDEX = 2;
const OUTPUT_GROUP = 3;

Object part1(String header, List input) {
  printHeader(header);
  var c = Computer(input);
  var blockTiles = <Point>{};
  while (!c.halted) {
    c.run([], true);
    var output = c.output();
    if (output.length == OUTPUT_GROUP) {
      c.output(true); //clear output
      if (output[TILE_ID_INDEX] == Tile.block.index) {
        blockTiles.add(Point(output[X_INDEX], output[Y_INDEX]));
      }
    }
  }
  return blockTiles.length;
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day13.txt', ',');

  printAndAssert(part1('13 part 1', mainInput), 273);
  // printAndAssert(part2('13 part 2', mainInput));
}
