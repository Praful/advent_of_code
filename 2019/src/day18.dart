import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import 'dart:collection';
import 'dart:math';
import 'package:tuple/tuple.dart';
import 'package:basics/basics.dart';

import 'test.dart';

/// Puzzle description: https://adventofcode.com/2019/day/18

const bool DEBUG = false;

const String PASSAGE = '.';
const String WALL = '#';
const String ENTRANCE = '@';

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

class Vault {
  final List _tunnelMap;
  final Set<String> _allDoorKeys = {}; //all keys eg a,b,c,etc
  Point _start;

  Vault(this._tunnelMap) {
    initialise();
  }

  //The List class is organised by row then col ie x and y are flipped.
  //So we put all access here to make sure we don't slip up.
  //Return what's located at p: wall, entrance, door key, door, or passage.
  String tunnelObject(p) => _tunnelMap[p.y][p.x];

  void initialise() {
    for (var y in range(0, _tunnelMap.length - 1)) {
      for (var x in range(0, _tunnelMap[0].length - 1)) {
        var char = tunnelObject(Point(x, y));
        if (isEntrance(char)) _start = Point(x, y);
        if (isDoorKey(char)) _allDoorKeys.add(char);
      }
    }
  }

  RegExp regexLowerCase = RegExp(r'^[a-z]$');
  RegExp regexUpperCase = RegExp(r'^[A-Z]$');
  bool isDoorKey(String s) => regexLowerCase.hasMatch(s);
  bool isDoor(String s) => regexUpperCase.hasMatch(s);
  bool isEntrance(String s) => s == ENTRANCE;
  bool isWall(String s) => s == WALL;

  int shortestPath() {
    var result = walk();
    print(result.item2);
    return result.item3;
  }

  QueuedNode walk() {
    var maxY = _tunnelMap.length - 1;
    var maxX = _tunnelMap[0].length - 1;

    bool isOnMap(Point p) => p.y.isBetween(0, maxY) && p.x.isBetween(0, maxX);
    bool canMoveTo(Point p) => !isWall(tunnelObject(p)) && isOnMap(p);
    bool isLockedDoor(Set keys, String s) =>
        (isDoor(s) && !keys.contains(s.toLowerCase()));

    String keysToStr(Set s) {
      var result = s.toList();
      result.sort();
      return result.join();
    }

    var queue = Queue<QueuedNode>();
    var visited = <VisitedNode>{};
    queue.add(QueuedNode(_start, <String>{}, 0));

    while (queue.isNotEmpty) {
      var qObj = queue.removeFirst();
      var visitId = VisitedNode(qObj.item1, keysToStr(qObj.item2));
      if (visited.contains(visitId)) continue;
      visited.add(visitId);

      var thing = tunnelObject(qObj.item1);
      if (isLockedDoor(qObj.item2, thing)) continue;

      var newDoorKeys = Set<String>.from(qObj.item2);

      if (isDoorKey(thing)) {
        newDoorKeys.add(thing);
        if (newDoorKeys.isEqualTo(_allDoorKeys)) return qObj;
      }

      adjacentPoints(qObj.item1).where((p) => canMoveTo(p)).forEach(
          (adjPt) => queue.add(QueuedNode(adjPt, newDoorKeys, qObj.item3 + 1)));
    }
    throw 'Shortest path not found';
  }
}

class QueuedNode extends Tuple3 {
  QueuedNode(Point p, Set<String> keys, int distance)
      : super(p, keys, distance);

  @override
  String toString() => '$item1, distance $item3, keys $item2';
}

class VisitedNode extends Tuple2 {
  VisitedNode(Point a, String b) : super(a, b);

  @override
  String toString() => '$item1, $item2';

  @override
  bool operator ==(other) =>
      other is VisitedNode && other.item1 == item1 && other.item2 == item2;
}

Object part1(String header, List input) {
  printHeader(header);

  return Vault(input).shortestPath();
}

Object part2(String header, List input) {
  printHeader(header);

  return null;
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/day18-test.txt'); //8
  List testInputb = FileUtils.asLines('../data/day18b-test.txt'); //86
  List testInputc = FileUtils.asLines(
      '../data/day18c-test.txt'); //132 steps: b, a, c, d, f, e, g

  // Shortest paths are 136 steps;
  // one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m
  List testInputd = FileUtils.asLines('../data/day18d-test.txt');

  // Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h
  List testInpute = FileUtils.asLines('../data/day18e-test.txt');

  List mainInput = FileUtils.asLines('../data/day18.txt');

  assertEqual(part1('18 test part 1', testInput), 8);
  assertEqual(part1('18 test part 1b', testInputb), 86);
  assertEqual(part1('18 test part 1c', testInputc), 132);
  assertEqual(part1('18 test part 1d', testInputd), 136);
  assertEqual(part1('18 test part 1e', testInpute), 81);
  // assertEqual(part2('18 test part 2', testInput), 1);

  printAndAssert(part1('18 part 1', mainInput), 6098);
  // printAndAssert(part2('18 part 2', mainInput));
}
