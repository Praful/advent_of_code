import '../../shared/dart/src/utils.dart';
import '../../shared/dart/src/grid.dart';
import 'dart:math';

/// Puzzle description: https://adventofcode.com/2019/day/24

const bool DEBUG = false;

const String BUG = '#';
const String SPACE = '.';

//centralise access to grid since x, y are col and row respectively, which
//may seem counter-intuitive.
String tileValue(grid, p) => grid[p.y][p.x];

int bugCount(List<String> grid, List<Point<int>> adj) {
  bool inGrid(Point<int> p) =>
      p.y.isBetween(0, grid.length - 1) && p.x.isBetween(0, grid[0].length - 1);

  var result = 0;
  for (var p in adj) {
    if (inGrid(p) && tileValue(grid, p) == BUG) result++;
  }
  return result;
}

List<String> evolve(List<String> grid) {
  var result = List<String>.from(grid);

  for (var r = 0; r < grid.length; r++) {
    for (var c = 0; c < grid[r].length; c++) {
      var tilePoint = Point<int>(c, r);
      var adj = adjacentPoints(tilePoint);
      var bugs = bugCount(grid, adj);

      var curState = tileValue(grid, tilePoint);
      var newState = curState;

      if (curState == BUG && bugs != 1) newState = SPACE;
      if (curState == SPACE && bugs.isBetween(1, 2)) newState = BUG;

      result[r] = result[r].replaceCharAt(c, newState);
    }
  }

  return result;
}

bool isPoint(Point<int> p, int x, int y) => p.x == x && p.y == y;
bool isCentre(Point<int> p) => isPoint(p, 2, 2);

int bugCount2(List<String> grid, List<String> subGrid, List<String> superGrid,
    Point<int> tile, List<Point<int>> adj) {
  bool inGrid(Point<int> p) =>
      (p.y).isBetween(0, grid.length - 1) &&
      (p.x).isBetween(0, grid[0].length - 1);

  var result = 0;
  for (var p in adj) {
    if (isCentre(p)) {
      //check subgrid
      //the part of the subgrid we check depends on the tile location ie
      //whether it's above, left of, right of or below the subgrid
      if (isPoint(tile, 1, 2)) {
        //left
        for (var i = 0; i < subGrid.length; i++) {
          if (tileValue(subGrid, Point<int>(0, i)) == BUG) result++;
        }
      } else if (isPoint(tile, 2, 1)) {
        //above
        for (var i = 0; i < subGrid[0].length; i++) {
          if (tileValue(subGrid, Point<int>(i, 0)) == BUG) result++;
        }
      } else if (isPoint(tile, 3, 2)) {
        //right
        for (var i = 0; i < subGrid.length; i++) {
          if (tileValue(subGrid, Point<int>(4, i)) == BUG) result++;
        }
      } else if (isPoint(tile, 2, 3)) {
        //below
        for (var i = 0; i < subGrid[0].length; i++) {
          if (tileValue(subGrid, Point<int>(i, 4)) == BUG) result++;
        }
      }
    } else if (inGrid(p)) {
      if (tileValue(grid, p) == BUG) result++;
    } else {
      //check supergrid
      //as above, the location of the tile determines where in the
      //side of the supergrid we check
      if (p.x == -1 && tileValue(superGrid, Point<int>(1, 2)) == BUG) result++;
      if (p.y == -1 && tileValue(superGrid, Point<int>(2, 1)) == BUG) result++;
      if (p.x == 5 && tileValue(superGrid, Point<int>(3, 2)) == BUG) result++;
      if (p.y == 5 && tileValue(superGrid, Point<int>(2, 3)) == BUG) result++;
    }
  }
  return result;
}

Map<int, List<String>> evolve2(Map<int, List<String>> levels, int minute) {
  var result = <int, List<String>>{};
  for (var levelId = (-minute / 2).ceil() - 1;
      levelId <= (minute / 2).ceil() + 1;
      levelId++) {
    var grid = levels[levelId]!;
    var evolvedGrid = List<String>.from(grid);
    for (var r = 0; r < grid.length; r++) {
      for (var c = 0; c < grid[r].length; c++) {
        var p = Point<int>(c, r);
        if (isCentre(p)) continue;
        var adj = adjacentPoints(p);
        var bugs =
            bugCount2(grid, levels[levelId + 1]!, levels[levelId - 1]!, p, adj);

        var curState = grid[r][c];
        var newState = curState;

        if (curState == BUG && bugs != 1) newState = SPACE;
        if (curState == SPACE && bugs.isBetween(1, 2)) newState = BUG;

        evolvedGrid[r] = evolvedGrid[r].replaceCharAt(c, newState);
      }
    }
    result[levelId] = evolvedGrid;
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

Map<int, List<String>> createNewLevels(int length, int levelCount) {
  List<String> newLevel(int length) {
    var result = <String>[];
    for (var i = 0; i < length; i++) {
      result.add(SPACE * length);
    }
    return result;
  }

  var blankGrid = newLevel(length);
  var levels = <int, List<String>>{};

  for (var i = 1; i < levelCount + 1; i++) {
    levels[i] = [...blankGrid];
    levels[-i] = [...blankGrid];
  }
  return levels;
}

int bugCountAllLevels(levels) {
  var result = 0;
  for (var grid in levels.values) {
    var s = grid.join();
    for (var i = 0; i < s.length; i++) {
      if (s[i] == BUG) result++;
    }
  }
  return result;
}

Object part1(String header, List<String> input) {
  printHeader(header);
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
}

Object part2(String header, List<String> input, int minutes) {
  printHeader(header);
  var levels = createNewLevels(input.length, (minutes / 2).ceil() + 2);
  levels[0] = input;

  for (var m = 0; m < minutes; m++) {
    var changedLevels = evolve2(levels, m);
    for (var kv in changedLevels.entries) {
      levels[kv.key] = kv.value;
    }
  }
  // levels.forEach((key, value) {
  //   print('level $key');
  //   printGrid(value);
  // });

  return bugCountAllLevels(levels);
}

void main(List<String> arguments) {
  var testInput = FileUtils.asLines('../data/day24-test.txt');
  var mainInput = FileUtils.asLines('../data/day24.txt');

  assertEqual(part1('24 test part 1', testInput), 2129920);
  assertEqual(part2('24 test part 2', testInput, 10), 99);

  printAndAssert(part1('24 part 1', mainInput), 17863711);
  printAndAssert(part2('24 part 2', mainInput, 200), 1937);
}
