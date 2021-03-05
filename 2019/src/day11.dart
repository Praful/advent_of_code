import 'dart:math';
import '../../shared/dart/src/utils.dart';
import 'intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/11

const bool DEBUG = false;

enum Turn { left, right }
enum Direction { north, east, south, west }
enum Panel { black, white }

class Robot {
  final Map<Point, Panel> _visitedPanels = {};
  final _program;
  Point _currentPosition = Point(0, 0);
  late Computer _computer;
  bool _firstRun = true;
  Direction _facing = Direction.north;
  late Panel _startPanelColour;
  late Panel _defaultPanelColour;

  Robot(this._program) {
    _computer = Computer(_program, () => ioProcessor());
  }

  void start([startPanelColour, defaultPanelColour]) {
    _defaultPanelColour = defaultPanelColour ?? Panel.black;
    _startPanelColour = startPanelColour ?? Panel.black;
    _computer.run();
  }

  List turnAndMove(turn) {
    var x = _currentPosition.x;
    var y = _currentPosition.y;

    switch (_facing) {
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
        throw 'Facing nowhere!';
    }

    var facing = turn == Turn.left
        ? Direction.values[(_facing.index - 1) % 4]
        : Direction.values[(_facing.index + 1) % 4];

    return [Point(x, y), facing];
  }

  //Provide input and process output of program being run by Robot.
  int ioProcessor() {
    var currentPanelColour;
    var output = _computer.output(true);

    if (output.isNotEmpty) {
      _visitedPanels[_currentPosition] = Panel.values[output[0]];
      var newLocation = turnAndMove(Turn.values[output[1]]);
      _currentPosition = newLocation[0];
      _facing = newLocation[1];
      currentPanelColour =
          _visitedPanels[_currentPosition] ?? _defaultPanelColour;
    } else {
      currentPanelColour = _firstRun ? _startPanelColour : _defaultPanelColour;
      if (_firstRun) _firstRun = false;
    }

    return currentPanelColour.index;
  }

  void printImage() {
    var pixel = {}
      ..[Panel.black] = '\u2588'
      ..[Panel.white] = '\u2591';

    var points = _visitedPanels.keys; //The panels the Robot went on.
    var cols =
        (points.map((v) => v.x).max - points.map((v) => v.x).min).abs() + 1 as int;
    var rows =
        (points.map((v) => v.y).min - points.map((v) => v.y).max).abs() + 1 as int;

    var image = TwoDimArray(rows, cols);

    //Initialise image's pixels to black
    range(0, rows)
        .forEach((row) => image[row] = (pixel[Panel.black] * cols).split(''));

    //Fill in white pixels: y's absolute values are taken because the image
    //coords start with (0,0) at top left.
    _visitedPanels.entries
        .where((kv) => kv.value == Panel.white)
        .forEach((p) => image[(p.key.y).abs() as int][p.key.x as int] = pixel[p.value]);

    //Print image
    image.forEach((row) => print(row.join()));
  }
}

Object part1(String header, List input) {
  printHeader(header);
  var r = Robot(input);
  r.start();
  return r._visitedPanels.length;
}

Object part2(String header, List input) {
  printHeader(header);
  var r = Robot(input);
  r.start(Panel.white, Panel.black);
  r.printImage();

  return '';
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day11.txt', ',');

  printAndAssert(part1('11 part 1', mainInput), 2373);
  printAndAssert(part2('11 part 2', mainInput)); //PCKRLPUK
}
