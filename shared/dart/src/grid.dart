import 'dart:math';
import 'utils.dart';

enum Direction { up, down, left, right }

Direction oppositeDirection(Direction dir) {
  switch (dir) {
    case Direction.up:
      return Direction.down;
    case Direction.down:
      return Direction.up;
    case Direction.left:
      return Direction.right;
    case Direction.right:
      return Direction.left;
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

List<Point<int>> adjacentPoints(Point<int> p) {
  var result = <Point<int>>[];
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
  final Point? xy;
  final Direction? dir;
  Position(this.xy, this.dir);

  bool get hasLocation => xy != null;
  bool get hasDirection => dir != null;

  @override
  String toString() => '$xy, $dir';
}

class Grid {}
