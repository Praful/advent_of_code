import '../../shared/dart/src/utils.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/3
///
/// Paths are given for two wires. The paths are in the
/// form <direction><steps> eg U34 to move right 34 steps. We take these
/// instructions and move, storing each coordinate passed through eg if
/// the first instruction is R3 we start at (0,0) then move to (1,0), (2,0)
/// and end up at (3,0). The next move starts at (3,0). Each
/// intermediate step is stored. This allows us later to work out
/// how many steps it took to get to a particular coordinate, which will
/// simply be the first index of that point in the path.
///
/// R is a move in the positive X-axis, L in the negative X-axis,
/// U is postive Y-axis and D is negative Y-axis.
///
/// Once we've noted all the points traversed by each wire, the intersection
/// of these two paths will provide where the wires cross.

const bool DEBUG = false;

//Captures a move, which consists of a direction and length.
class Move {
  final direction, steps;
  static final oneStep = {}
    ..['R'] = Point(1, 0)
    ..['L'] = Point(-1, 0)
    ..['U'] = Point(0, 1)
    ..['D'] = Point(0, -1);

  static const origin = Point(0, 0);

  Move(this.direction, this.steps);

  static final RegExp regex = RegExp(r'(?<direction>.)(?<steps>\d*)');
  static Move parse(s) {
    var parsed = regex.firstMatch(s);
    return Move(
        parsed.namedGroup('direction'), parsed.namedGroup('steps').toInt());
  }

  @override
  String toString() => '$direction, $steps';
}

class Wire {
  List<Move> path;

  Wire(input) {
    path = parse(input);
  }

  List<Move> parse(List input) => input.map((s) => Move.parse(s)).toList();

  //For all moves (eg R3, U5, D5, etc), return all the points we go
  //through to get to the last point. We use expand() because after doing the
  //map we'll have a list of lists and want to flatten out to just be a list
  //of points.
  List<Point> navigate([location = Move.origin]) => path
      .map((move) {
        var moves = doMove(location, move);
        location = moves.last;
        return moves;
      })
      .expand((e) => e)
      .toList();

  //For a move, eg R15, return a list of points we go through to get to
  //the final point, which for R15 is 15 steps to the right of the
  //start point and therefore the result will have 15 point objects.
  List<Point> doMove(Point start, Move move) => range(1, move.steps + 1)
      .map((steps) => start + (Move.oneStep[move.direction] * steps))
      .toList();
}

int manhattan(Point p) => p.x.abs() + p.y.abs();

int minManhattan(List<Point> path1, List<Point> path2) =>
    path1.toSet().intersection(path2.toSet()).map((p) => manhattan(p)).min;

//Return number of steps to first occurence of point.
int minSteps(List<Point> path, Point p) => path.indexOf(p) + 1;

int minStepsToCrossings(List<Point> path1, List<Point> path2) => path1
    .toSet()
    .intersection(path2.toSet())
    .map((p) => minSteps(path1, p) + minSteps(path2, p))
    .min;

int part1(String header, List<String> input) {
  printHeader(header);
  var w1 = Wire(input[0].split(','));
  var w2 = Wire(input[1].split(','));
  return minManhattan(w1.navigate(), w2.navigate());
}

int part2(String header, List<String> input) {
  printHeader(header);
  var w1 = Wire(input[0].split(','));
  var w2 = Wire(input[1].split(','));
  return minStepsToCrossings(w1.navigate(), w2.navigate());
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/day03-test.txt');
  List testInput3b = FileUtils.asLines('../data/day03b-test.txt');
  List testInput3c = FileUtils.asLines('../data/day03c-test.txt');
  List mainInput = FileUtils.asLines('../data/day03.txt');

  assertEqual(part1('03 test part 1', testInput), 6);
  assertEqual(part1('03 test part 1b', testInput3b), 159);
  assertEqual(part1('03 test part 1c', testInput3c), 135);

  assertEqual(part2('03 test part 2', testInput), 30);
  assertEqual(part2('03 test part 2b', testInput3b), 610);
  assertEqual(part2('03 test part 2c', testInput3c), 410);

  print(part1('03 part 1', mainInput)); //1519
  print(part2('03 part 2', mainInput)); //14358
}
