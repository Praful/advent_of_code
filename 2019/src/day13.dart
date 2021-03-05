import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/4

const bool DEBUG = false;

enum Tile { empty, wall, block, paddle, ball }
const X = 0;
const Y = 1;
const TILE = 2;
const INSTRUCTION_LENGTH = 3;

class Game {
  static const MOVE_LEFT = -1;
  static const MOVE_RIGHT = 1;
  static const MOVE_NONE = 0;

  final input;
  // List<List<int>> output;
  late Point ballPosition;
  late Point paddlePosition;

  Game(this.input);

  int inputProvider() => (ballPosition.x - paddlePosition.x).sign as int;

  int play() {
    input[0] = 2; //initialise game
    late int score;
    var c = Computer(input, () => inputProvider());
    while (!c.halted) {
      c.run([], true);
      var output = c.output();
      if (output.length == INSTRUCTION_LENGTH) {
        c.output(true); //clear output
        if (output[TILE] == Tile.ball.index) {
          ballPosition = Point(output[X], output[Y]);
        } else if (output[TILE] == Tile.paddle.index) {
          paddlePosition = Point(output[X], output[Y]);
        } else if (output[X] == -1 && output[Y] == 0) {
          score = output[TILE];
        }
      }
    }
    return score;
  }
}

Object part1(String header, List<int> program) {
  printHeader(header);
  var c = Computer(program);
  var blockTiles = <Point>{};
  while (!c.halted) {
    c.run([], true);
    var output = c.output();
    if (output.length == INSTRUCTION_LENGTH) {
      c.output(true); //clear output
      if (output[TILE] == Tile.block.index) {
        blockTiles.add(Point(output[X], output[Y]));
      }
    }
  }
  return blockTiles.length;
}

Object part2(String header, List input) {
  printHeader(header);
  return Game(input).play();
}

void main(List<String> arguments) {
  var mainInput = FileUtils.asInt('../data/day13.txt', ',');

  printAndAssert(part1('13 part 1', mainInput), 273);
  printAndAssert(part2('13 part 2', mainInput), 13140);
}
