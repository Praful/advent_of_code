import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import 'dart:collection';
import 'dart:math';
import 'package:tuple/tuple.dart';

/// Puzzle description: https://adventofcode.com/2019/day/20
/// Uses BFS to walk maze.

const bool DEBUG = false;

const String PASSAGE = '.';
const String WALL = '#';

class Maze {
  final List _maze;
  late final Point<int> _start;
  late final Point<int> _end;
  late final Map<Point<int>, Point<int>> _portalMapping;

  Maze(this._maze) {
    _portalMapping = findPortals(_maze);
  }

  //The List class is organised by row then col ie x and y are flipped.
  //So we put all access here to make sure we don't slip up.
  //Return thing at p: wall, space, or passage.
  String mazeTile(Point p) => _maze[p.y.toInt()][p.x.toInt()];

  List<String> possiblePortals(int x, int y) => [
        mazeTile(Point<int>(x, y - 2)) + mazeTile(Point<int>(x, y - 1)),
        mazeTile(Point<int>(x + 1, y)) + mazeTile(Point<int>(x + 2, y)),
        mazeTile(Point<int>(x, y + 1)) + mazeTile(Point<int>(x, y + 2)),
        mazeTile(Point<int>(x - 2, y)) + mazeTile(Point<int>(x - 1, y))
      ];

  Map<Point<int>, Point<int>> findPortals(maze) {
    var result = <Point<int>, Point<int>>{};
    var portals = <String, Point<int>>{};

    for (var y in range(0, maze.length - 1)) {
      for (var x in range(0, maze[0].length - 1)) {
        var p = Point<int>(x, y);
        if (isPassage(p)) {
          for (var candidatePortal in possiblePortals(x, y)) {
            if (isPortal(candidatePortal)) {
              if (candidatePortal == 'AA') {
                _start = p;
                continue;
              }
              if (candidatePortal == 'ZZ') {
                _end = p;
                continue;
              }

              var pp = portals[candidatePortal];
              //if we have one end of portal, map to the just found other end.
              if (pp != null) {
                result[pp] = p;
                result[p] = pp;
              } else {
                portals[candidatePortal] = p;
              }
            }
          }
        }
      }
    }
    return result;
  }

  bool isPortal(String s) => RegExp(r'^[A-Z][A-Z]$').hasMatch(s);
  bool isWall(String s) => s == WALL;
  bool isPassage(Point p) => mazeTile(p) == PASSAGE;

  int shortestPath1() {
    var result = walk1();
    return result.item3;
  }

  int shortestPath2() {
    var result = walk2();
    return result.item3;
  }

  QueuedNode walk1() {
    var queue = Queue<QueuedNode>();
    var visited = <VisitedNode>{};

    queue.add(QueuedNode(_start, 0, 0));

    while (queue.isNotEmpty) {
      var qObj = queue.removeFirst();

      if (qObj.location == _end) return qObj;

      var visitId = VisitedNode(qObj.location, 0);
      if (visited.contains(visitId)) continue;
      visited.add(visitId);

      queue.addAll(adjacentPoints(qObj.location)
          .where((p) => isPassage(p))
          .map((adjPt) => QueuedNode(adjPt, 0, qObj.steps + 1)));

      var pp = _portalMapping[qObj.location];
      if (pp != null) queue.add(QueuedNode(pp, 0, qObj.steps + 1));
    }
    throw 'Shortest path not found';
  }

  QueuedNode walk2() {
    var queue = Queue<QueuedNode>();
    var visited = <VisitedNode>{};
    const BORDER = 4;

    bool isInnerPortal(Point? p) =>
        p != null &&
        p.x.isBetween(BORDER, _maze[0].length - BORDER) &&
        p.y.isBetween(BORDER, _maze.length - BORDER);

    queue.add(QueuedNode(_start, 0, 0));

    while (queue.isNotEmpty) {
      var qObj = queue.removeFirst();

      if (qObj.location == _end && qObj.level == 0) return qObj;

      var visitId = VisitedNode(qObj.location, qObj.level);
      if (visited.contains(visitId)) continue;
      visited.add(visitId);

      queue.addAll(adjacentPoints(qObj.location)
          .where((p) => isPassage(p))
          .map((adjPt) => QueuedNode(adjPt, qObj.level, qObj.steps + 1)));

      var pp = _portalMapping[qObj.location];
      if (pp != null) {
        if (isInnerPortal(qObj.location)) {
          queue.add(QueuedNode(pp, qObj.level + 1, qObj.steps + 1));
        }
        //outer portals don't apply at level 0
        else if (qObj.level > 0) {
          queue.add(QueuedNode(pp, qObj.level - 1, qObj.steps + 1));
        }
      }
    }
    throw 'Shortest path not found';
  }
}

class QueuedNode extends Tuple3 {
  QueuedNode(Point<int>? location, int level, int steps)
      : super(location, level, steps);

  Point<int> get location => item1;
  int get level => item2;
  int get steps => item3;

  @override
  String toString() => 'location $item1, steps $item3, level $item2';
}

Function isInnerPortal(minX, maxX, minY, maxY) =>
    (Point<int> p) => p.x.isBetween(minX, maxX) && p.y.isBetween(minY, maxY);

class VisitedNode extends Tuple2 {
  VisitedNode(Point<int> location, int level) : super(location, level);

  Point<int> get location => item1;
  int get level => item2;

  @override
  String toString() => 'location $item1, level $item2';

  @override
  bool operator ==(other) =>
      other is VisitedNode && other.item1 == item1 && other.item2 == item2;
}

int part1(String header, List input) {
  printHeader(header);
  return Maze(input).shortestPath1();
}

Object part2(String header, List input) {
  printHeader(header);
  return Maze(input).shortestPath2();
}

void main(List<String> arguments) {
  var testInput = FileUtils.asLines('../data/day20-test.txt');
  var testInput1b = FileUtils.asLines('../data/day20b-test.txt');
  var testInput2c = FileUtils.asLines('../data/day20c-test.txt');
  var mainInput = FileUtils.asLines('../data/day20.txt');

  assertEqual(part1('20 test part 1', testInput), 23);
  assertEqual(part1('20 test part 1b', testInput1b), 58);

  assertEqual(part2('20 test part 2', testInput), 26);
  assertEqual(part2('20 test part 2c', testInput2c), 396);

  printAndAssert(part1('20 part 1', mainInput), 714);
  printAndAssert(part2('20 part 2', mainInput), 7876);
}
