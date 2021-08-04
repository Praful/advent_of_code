import 'dart:collection';

import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/15
///
/// Despite appearances, BFS is used to find the shortest path. There is a
/// complication because with BFS you can see where you're moving to. In this
/// case, the droid tells after you attempt to move what you've
/// encountered: a wall, a valid path or the target (oxygen).
/// But the algorithm is the same: for a given spot, enqueue the places
/// you can travel to. For each of those places, do the same, incrementing
/// the distance counter the further you are from the starting point.
/// Because the droid actually moves (when you legimately can), you have to
/// go back to where you were to check the other adjacent enqueued points.
/// This is done by saving the Computer object's state and restoring it
/// when examining a location.

const bool DEBUG = false;

class TraversalResult {
  final visited, oxygenLocation, shortestPath;
  TraversalResult(this.visited, this.oxygenLocation, this.shortestPath);
}

class Node {
  Point location;
  Direction? direction;
  int distance;
  ComputerState computerState;

  Node(this.location, this.direction, this.distance, this.computerState);

  @override
  String toString() =>
      'location: $location, direction: $direction, distance: $distance';
}

enum Direction { north, south, west, east }

enum DroidStatus { wall, path, oxygen, unknown }

class SpaceStation {
  final _input;
  final Point _start = Point(0, 0);
  final Queue<Node> _exploreQueue = Queue();
  late final Computer _droid;

  SpaceStation(this._input) {
    _droid = Computer(_input);
  }

  void printLayout(Map<Point, DroidStatus> visited, oxygenLocation) {
    var pixel = {}
      ..[DroidStatus.wall] = '\u2588' // '#'
      ..[DroidStatus.path] = '.'
      ..[DroidStatus.oxygen] = 'O'; //'\u2591';

    var points = visited.keys;
    var xmin = points.map((v) => v.x).min;
    var ymin = points.map((v) => v.y).min;

    var cols =
        (points.map((v) => v.x).max - points.map((v) => v.x).min).abs() + 1 as int;
    var rows =
        (points.map((v) => v.y).min - points.map((v) => v.y).max).abs() + 1 as int;

    var image = TwoDimArray(rows, cols);

    //Initialise image's pixels to space
    range(0, rows).forEach((row) => image[row] = (' ' * cols).split(''));
    visited.entries.forEach((p) => image[(p.key.y + ymin.abs()).abs() as int]
        [p.key.x + xmin.abs() as int] = pixel[p.value]);

    //start/end
    image[0 + ymin.abs() as int][0 + xmin.abs() as int] = 'S';
    if (oxygenLocation != null) {
      image[oxygenLocation.y + ymin.abs()][oxygenLocation.x + xmin.abs()] = 'O';
    }

    //Print image. The 'reverse' is to orient the image with
    //north up and south down. Emperically determined.
    image.reversed.forEach((row) => print(row.join()));
  }

  bool canMoveTo(visited, p) => !visited.containsKey(p);

  void enqueueAdjacent(Map visited, Node n) {
    for (var dir in Direction.values) {
      var adjPos = coords(n.location, dir);
      if (canMoveTo(visited, adjPos)) {
        _exploreQueue
            .add(Node(n.location, dir, n.distance + 1, n.computerState));
      }
    }
  }

  void addVisit(visited, previousNode, previousOutput) =>
      visited[coords(previousNode.location, previousNode.direction)] =
          previousOutput;

  Node? nextMove(visited, previousNode, previousOutput) {
    //If we moved last time, get current locaton and enqueue its adjacent
    //nodes to explore later
    if (previousOutput == DroidStatus.path) {
      var newLocation = coords(previousNode.location, previousNode.direction);
      enqueueAdjacent(visited,
          Node(newLocation, null, previousNode.distance, _droid.state));
    }
    return _exploreQueue.isEmpty ? null : _exploreQueue.removeFirst();
  }

  //Return coords if we moved from 'from' in direction 'directionOfTravel'
  Point coords(Point from, Direction directionOfTravel) {
    var result;
    switch (directionOfTravel) {
      case Direction.north:
        result = Point(from.x, from.y + 1);
        break;
      case Direction.south:
        result = Point(from.x, from.y - 1);
        break;
      case Direction.west:
        result = Point(from.x - 1, from.y);
        break;
      case Direction.east:
        result = Point(from.x + 1, from.y);
        break;
      default:
        throw 'Direction unknown';
    }
    return result;
  }

  TraversalResult shortestPath() => traverse();

  TraversalResult traverse([bool stopWhenOxygenFound = true]) {
    var visited = <Point, DroidStatus>{};
    var previousNode;
    var previousOutput;
    enqueueAdjacent(visited, Node(_start, null, 0, _droid.state));
    visited[_start] = DroidStatus.path;

    while (!_droid.halted) {
      if (stopWhenOxygenFound && previousOutput == DroidStatus.oxygen) break;

      var nextNode = nextMove(visited, previousNode, previousOutput);
      if (nextNode == null) break;

      _droid
        ..input = nextNode.direction!.index + 1
        ..state = nextNode.computerState
        ..run([], true);

      previousNode = nextNode;

      if (_droid.output().isNotEmpty) {
        previousOutput = DroidStatus.values[_droid.output(true)[0]];
      }

      if (previousOutput != null) {
        addVisit(visited, previousNode, previousOutput);
      }
    }

    var oxygenLocation = stopWhenOxygenFound
        ? coords(previousNode.location, previousNode.direction)
        : null;

    printLayout(visited, oxygenLocation);

    return TraversalResult(visited, oxygenLocation, previousNode.distance);
  }

  int fillWithOxygen(oxygenLocation) {
    var traversalResult = traverse(false);
    var path =
        Map<Point, DroidStatus>.fromEntries(traversalResult.visited.entries);

    bool isPath(p) => path.containsKey(p) && path[p] == DroidStatus.path;

    var minutes = 0;
    var nextQueue = Queue()..add(oxygenLocation);
    path[oxygenLocation] = DroidStatus.oxygen;

    while (nextQueue.isNotEmpty) {
      minutes++;
      var currentQueue = Queue.from(nextQueue);
      nextQueue.clear();

      while (currentQueue.isNotEmpty) {
        var location = currentQueue.removeFirst();
        for (var dir in Direction.values) {
          var adj = coords(location, dir);
          if (isPath(adj)) {
            path[adj] = DroidStatus.oxygen;
            nextQueue.add(adj);
          }
        }
      }
    }

    printLayout(path, oxygenLocation);

    //subtract 1 to exclude the starting point, which has oxygen
    return minutes - 1;
  }
}

TraversalResult part1(String header, List input) {
  printHeader(header);
  var station = SpaceStation(input);
  return station.shortestPath();
}

int part2(String header, List input, oxygenLocation) {
  printHeader(header);
  var station = SpaceStation(input);
  return station.fillWithOxygen(oxygenLocation);
}

void main(List<String> arguments) {
  List mainInput = FileUtils.asInt('../data/day15.txt', ',');
  var part1Result = part1('15 part 1', mainInput);
  print('Oxygen location: ${part1Result.oxygenLocation}');
  printAndAssert(part1Result.shortestPath, 204);
  printAndAssert(
      part2('15 part 2', mainInput, part1Result.oxygenLocation), 340);
}
