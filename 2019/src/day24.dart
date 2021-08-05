import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/24

const bool DEBUG = false;

const String BUG = '#';
const String SPACE = '.';

int bugCount(List<String> grid, List<Point> points) {
  bool inGrid(p) =>
      (p.x as int).isBetween(0, grid.length - 1) &&
      (p.y as int).isBetween(0, grid[0].length - 1);

  var result = 0;
  for (var p in points) {
    if (inGrid(p) && (grid[p.x as int][p.y as int] == BUG)) result++;
  }
  return result;
}

List<String> evolve(List<String> grid) {
  var result = List<String>.from(grid);

  for (var r = 0; r < grid.length; r++) {
    for (var c = 0; c < grid[r].length; c++) {
      var adj = adjacentPoints(Point(r, c));
      var bugs = bugCount(grid, adj);

      var curState = grid[r][c];
      var newState = curState;

      if (curState == BUG && bugs != 1) newState = SPACE;
      if (curState == SPACE && bugs.isBetween(1, 2)) newState = BUG;

      // print('$r, $c: $curState, $newState');

      result[r] = result[r].replaceCharAt(c, newState);
    }
  }

  return result;
}

int biodiversity(List<String> grid) {
  var result = 0;
  var s = grid.join();
  for (var i = 0; i < s.length; i++) {
    if (s[i] == BUG) result += pow(2, i) as int;
  }
  return result;
}

Object part1(String header, List<String> input) {
  printHeader(header);
  // printGrid(input);
  var biodiversityHistory = <int>{};

  var grid = input;

  while (true) {
    // print('----------------');
    grid = evolve(grid);
    // printGrid(grid);
    var bd = biodiversity(grid);
    if (biodiversityHistory.contains(bd)) return bd;
    biodiversityHistory.add(bd);
  }
  // return 0;
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return 0;
}

void main(List<String> arguments) {
  var testInput = FileUtils.asLines('../data/day24-test.txt');
  var mainInput = FileUtils.asLines('../data/day24.txt');

  assertEqual(part1('24 test part 1', testInput), 2129920);
  // assertEqual(part2('24 test part 2', testInput), 1);

  printAndAssert(part1('24 part 1', mainInput), 17863711);
  // printAndAssert(part2('24 part 2', mainInput));
}
