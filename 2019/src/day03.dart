import '../../shared/dart/src/utils.dart';
import 'dart:math';

const bool DEBUG = false;

class Move {
  final direction, steps;
  static final changeVector = {}
    ..['R'] = Point(1, 0)
    ..['L'] = Point(-1, 0)
    ..['U'] = Point(0, 1)
    ..['D'] = Point(0, -1);

  Move(this.direction, this.steps);

  static RegExp regex = RegExp(r'(?<direction>.)(?<steps>\d*)');
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

  List<Point> navigate() {
    var visited = <Point>[];
    var location = Point(0, 0);
    path.forEach((move) {
      visited.addAll(doMove(location, move));
      location += Move.changeVector[move.direction] * move.steps;
    });
    return visited;
  }

  //Return list of points we've gone through to move to new location.
  List<Point> doMove(Point start, Move move) {
    var visited = <Point>[];
    var current = start;
    range(0, move.steps).forEach((_) {
      current += Move.changeVector[move.direction];
      visited.add(current);
    });
    return visited;
  }
}

int manhattan(Point p) => p.x.abs() + p.y.abs();

int minManhattan(List<Point> path1, List<Point> path2) =>
    path1.toSet().intersection(path2.toSet()).map((p) => manhattan(p)).min;

int minSteps(List<Point> path, Point p) => path.indexOf(p) + 1;

int minStepsToCrossings(List<Point> path1, List<Point> path2) => path1
    .toSet()
    .intersection(path2.toSet())
    .map((p) => minSteps(path1, p) + minSteps(path2, p))
    .min;

int part1(String name, List<String> input) {
  printHeader(name);
  var w1 = Wire(input[0].split(','));
  var w2 = Wire(input[1].split(','));
  return minManhattan(w1.navigate(), w2.navigate());
}

int part2(String name, List<String> input) {
  printHeader(name);
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
