import 'dart:math';
import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';

/// Puzzle description: https://adventofcode.com/2019/day/10

///For part 1: go through each pair of points and see if another
///point is between them. Incrememt a counter for each pair if nothing
///is between them.
///
///For part 2: work out the angle of each point from the vertical axis
///of the monitoring station. Order points at the same angle according 
///to their distance from the monitoring station.
const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

class MonitoringStation {
  static const ASTEROID = '#';
  static const DELTA = 0.000000001;
  final List<String> aerialMap;
  List<Point> asteroids = [];
  Map<Point, Set<Point>> visited = {};

  MonitoringStation(this.aerialMap) {
    asteroids = asteroidCoords();
  }

  List asteroidCoords() {
    var result = <Point>[];
    aerialMap.asMap().entries.forEach((entry) {
      var y = entry.key;
      for (var x = 0; x < entry.value.length; x++) {
        if (entry.value[x] == ASTEROID) result.add(Point(x, y));
      }
    });
    return result;
  }

  //Return true if c lies on line between a and b.
  bool isBetween(Point a, Point b, Point c) =>
      a.distanceTo(c) + b.distanceTo(c) - a.distanceTo(b) < DELTA;

  //Return true if there are no points between a and b.
  bool hasDirectLine(Point a, Point b) {
    for (var c in asteroids) {
      if (a == c || b == c) continue;
      if (isBetween(a, b, c)) return false;
    }

    return true;
  }

  int maxAsteroidsVisible() {
    var visible = <Point, int>{};
    Combinations(2, asteroids)().forEach((pair) {
      if (hasDirectLine(pair[0], pair[1])) {
        visible[pair[0]] = (visible[pair[0]] ?? 0) + 1;
        visible[pair[1]] = (visible[pair[1]] ?? 0) + 1;
      }
    });
    var max = visible.values.max;
    visible.entries.forEach((kv) {
      if (kv.value == max) print(kv.key);
    });
    return visible.values.max;
  }

  // See https://stackoverflow.com/questions/3486172/angle-between-3-points
  //If a, b, c are a triangle, return angle at point b ie angle between
  //ba and bc.
  num angleBetween(Point a, Point b, Point c) {
    var ab = Point(b.x - a.x, b.y - a.y);
    var cb = Point(b.x - c.x, b.y - c.y);

    var dot = (ab.x * cb.x + ab.y * cb.y); // dot product
    var cross = (ab.x * cb.y - ab.y * cb.x); // cross product
    var alpha = atan2(cross, dot);

    var angle = alpha * 180 / pi;
    if (angle < 0) angle += 360;
    return angle;
  }

  //Work out angles between line ba and line bc
  //where c is successively the other asteroids on the map.
  //Points at the same angle are arranged in distance order from b.
  Map<String, List<Point>> angledPoints(Point b, Point a) {
    var result = <String, List<Point>>{};
    for (var c in asteroids) {
      if (b == c) continue;
      var angle = angleBetween(a, b, c).toStringAsFixed(3);
      var aligned = result[angle] ?? <Point>[];
      aligned.add(c);
      result[angle] = aligned;
    }

    result.values.forEach((l) => l.sort((p1, p2) =>
        b.squaredDistanceTo(p1) < b.squaredDistanceTo(p2) ? -1 : 1));

    return result;
  }

  Point vaporize(Point monitoringStationLocation, int vaporizeCount) {
    var result;
    var vaporized = 0;
    var northPoint = Point(monitoringStationLocation.x, 0);
    var pointAngles = angledPoints(monitoringStationLocation, northPoint);
    var pointAnglesSorted = pointAngles.keys.toList()
      ..sort((a, b) => a.toDouble() < b.toDouble() ? -1 : 1);

    while (vaporized < vaporizeCount) {
      for (var angle in pointAnglesSorted) {
        var aligned = pointAngles[angle];
        if (aligned.isNotEmpty) {
          result = aligned.removeAt(0);
          vaporized++;
          if (vaporized >= vaporizeCount) break;
        }
      }
    }
    return result;
  }
}

Object part1(String header, List input) {
  printHeader(header);
  var ms = MonitoringStation(input);
  return ms.maxAsteroidsVisible();
}

Object part2(String header, List input, Point location, vaporizeCount) {
  printHeader(header);
  var ms = MonitoringStation(input);
  var result = ms.vaporize(location, vaporizeCount);
  return result.x * 100 + result.y;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/day10-test.txt');
  List testInputb = FileUtils.asLines('../data/day10b-test.txt');
  List testInputc = FileUtils.asLines('../data/day10c-test.txt');
  List testInputd = FileUtils.asLines('../data/day10d-test.txt');
  List testInpute = FileUtils.asLines('../data/day10e-test.txt');

  // List testInputf = FileUtils.asLines('../data/day10f-test.txt');

  List mainInput = FileUtils.asLines('../data/day10.txt');

  assertEqual(part1('10 test part 1', testInput), 8); //(3,4)
  assertEqual(part1('10 test part 1b', testInputb), 33); //(5,8)
  assertEqual(part1('10 test part 1c', testInputc), 35); //(1,2)
  assertEqual(part1('10 test part 1d', testInputd), 41); //(6,3)
  assertEqual(part1('10 test part 1e', testInpute), 210); //(11,13)

  assertEqual(part2('10 test part 2', testInpute, Point(11, 13), 200), 802);

  printAndAssert(part1('10 part 1', mainInput), 256); // (29, 28)
  printAndAssert(part2('10 part 2', mainInput, Point(29, 28), 200), 1707);
}
