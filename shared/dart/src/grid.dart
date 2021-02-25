import 'dart:math';
import 'utils.dart';

enum Direction { up, down, left, right }

Direction oppositeDirection(Direction dir) {
  switch (dir) {
    case Direction.up:
      return Direction.down;
      break;
    case Direction.down:
      return Direction.up;
      break;
    case Direction.left:
      return Direction.right;
      break;
    case Direction.right:
      return Direction.left;
      break;
    default:
      throw 'Unrecognised direction $dir';
  }
}

final adjacentVector = {}
  ..[Direction.right] = Point(1, 0)
  ..[Direction.left] = Point(-1, 0)
  ..[Direction.up] = Point(0, -1)
  ..[Direction.down] = Point(0, 1);

final Map<Direction, Direction> rightTurns = {
  Direction.up: Direction.right,
  Direction.down: Direction.left,
  Direction.right: Direction.down,
  Direction.left: Direction.up
};

List<Point> adjacentPoints(Point p) {
  var result = <Point>[];
  for (var dir in Direction.values) {
    var adjPos = p + adjacentVector[dir];
    // if (isValid(adjPos)) result.add(adjPos);
    result.add(adjPos);
  }
  return result;
}

void printGrid(List<String> g) {
  for (var row in range(0, g.length)) {
    print(g[row]);
  }
}

class Node {
  Point location;
  Direction direction;
  int distance;
  int state;

  Node(this.location, this.direction, this.distance, this.state);

  @override
  String toString() =>
      'location: $location, direction: $direction, distance: $distance';
}

class Position {
  final Point xy;
  final Direction dir;
  Position(this.xy, this.dir);

  bool get hasLocation => xy != null;
  bool get hasDirection => dir != null;

  @override
  String toString() => '$xy, $dir';
}

class Grid {}
