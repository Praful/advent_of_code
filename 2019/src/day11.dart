import 'dart:math';
import '../../shared/dart/src/utils.dart';
import 'intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/11

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

enum Turn { left, right }
enum Direction { north, east, south, west }

class Robot {
  Map<Point, int> grid = {};
  static const BLACK_PANEL = 0;
  static const WHITE_PANEL = 1;
  final program;
  Point currentPosition = Point(0, 0);
  Computer computer;
  bool _firstRun = true;
  Direction facing = Direction.north;
  int _startPanelColour;
  int _defaultPanelColour;

  Robot(this.program) {
    computer = Computer(program, () => ioProcessor());
  }

  void start(
      [startPanelColour = BLACK_PANEL, defaultPanelColour = BLACK_PANEL]) {
    _defaultPanelColour = defaultPanelColour;
    _startPanelColour = startPanelColour;
    computer.run();
  }

  Point TurnAndMove(turn) {
    var x = currentPosition.x;
    var y = currentPosition.y;

    switch (facing) {
      case Direction.north:
        x = x + (turn == Turn.left ? -1 : 1);
        break;
      case Direction.east:
        y = y + (turn == Turn.left ? 1 : -1);
        break;
      case Direction.south:
        x = x + (turn == Turn.left ? 1 : -1);
        break;
      case Direction.west:
        y = y + (turn == Turn.left ? -1 : 1);
        break;
      default:
        throw 'Facing nowhere';
    }

    facing = turn == Turn.left
        ? Direction.values[(facing.index - 1) % 4]
        : Direction.values[(facing.index + 1) % 4];

    return Point(x, y);
  }

  //Provide input and process output of program being run by Robot.
  int ioProcessor() {
    var currentPanelColour;
    var output = computer.output(true);

    if (output.isNotEmpty) {
      grid[currentPosition] = output[0];
      currentPosition = TurnAndMove(output[1] == 0 ? Turn.left : Turn.right);
      currentPanelColour = grid[currentPosition] ?? _defaultPanelColour;
    } else {
      currentPanelColour = _firstRun ? _startPanelColour : _defaultPanelColour;
      if (_firstRun) _firstRun = false;
    }
    return currentPanelColour;
  }

  void printImage() {
    var pixel = {}
      ..[BLACK_PANEL] = '\u2588'
      ..[WHITE_PANEL] = '\u2591';

    var points = grid.keys; //The panels the Robot went on.
    var cols =
        (points.map((v) => v.x).max - points.map((v) => v.x).min).abs() + 1;
    var rows =
        (points.map((v) => v.y).min - points.map((v) => v.y).max).abs() + 1;

    var image = TwoDimArray(rows, cols);

    //Initialise image's pixels to black
    range(0, rows)
        .forEach((row) => image[row] = (pixel[BLACK_PANEL] * cols).split(''));

    //Fill in white pixels: y's absolute values are taken because the image
    //coords start with (0,0) at top left.
    grid.entries
        .where((kv) => kv.value == WHITE_PANEL)
        .forEach((p) => image[(p.key.y).abs()][p.key.x] = pixel[p.value]);

    //Print image
    image.forEach((row) => print(row.join()));
  }
}

Object part1(String header, List input) {
  printHeader(header);
  var r = Robot(input);
  r.start();
  return r.grid.length;
}

Object part2(String header, List input) {
  printHeader(header);
  var r = Robot(input);
  r.start(Robot.WHITE_PANEL, Robot.BLACK_PANEL);
  r.printImage();

  return '';
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day11.txt', ',');

  printAndAssert(part1('11 part 1', mainInput), 2373);
  printAndAssert(part2('11 part 2', mainInput)); //PCKRLPUK
}
