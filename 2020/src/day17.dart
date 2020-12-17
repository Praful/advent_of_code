import './utils.dart';
import 'dart:math' as math;

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

class Point {
  final int x;
  final int y;
  final int z;
  Point(this.x, this.y, this.z);

  @override
  String toString() => '$x,$y,$z';
  static Point toPoint(String s) {
    var coord = s.split(',').map((c) => int.parse(c)).toList();
    return Point(coord[0], coord[1], coord[2]);
  }

  bool operator ==(covariant Point other) =>
      x == other.x && y == other.y && z == other.z;
}

class PocketDimension {
  List input;
  Map<String, String> _grid = {};
  static const String ACTIVE = '#';
  static const String INACTIVE = '.';

  var xMinMax;
  var yMinMax;
  var zMinMax;

  PocketDimension(this.input) {
    toGrid();
  }

  String toKey(x, y, z) => Point(x, y, z).toString();

  void toGrid() {
    var x = 0, y = 0, z = 0;

    input.forEach((row) {
      row.split('').forEach((c) {
        if (c == ACTIVE) makeActive(_grid, Point(x, y, z));
        x += 1;
      });
      x = 0;
      y += 1;
    });
    xMinMax = [0, input[0].length - 1];
    yMinMax = [0, input.length - 1];
    zMinMax = [0, 0];
  }

  @override
  String toString() => '$_grid';

  int activeCubes() => _grid.keys.length;

  int activeNeighbours(Point target) {
    var activeCount = 0;
    for (var x = target.x - 1; x < target.x + 2; x++) {
      for (var y = target.y - 1; y < target.y + 2; y++) {
        for (var z = target.z - 1; z < target.z + 2; z++) {
          var neighbour = Point(x, y, z);
          if (target == neighbour) continue;
          if (isActive(neighbour)) activeCount++;
        }
      }
    }
    return activeCount;
  }

  List minMax(int dimension) {
    var min, max;

    void update(v) {
      min = min ?? v;
      if (v < min) min = v;
      max = max ?? v;
      if (v > max) max = v;
    }

    _grid.keys.forEach((k) {
      var p = Point.toPoint(k);
      switch (dimension) {
        case 0:
          update(p.x);
          break;
        case 1:
          update(p.y);
          break;
        case 2:
          update(p.z);
          break;
        default:
      }
    });
    return [min - 1, max + 1];
  }

  void makeActive(grid, Point p) => grid[p.toString()] = ACTIVE;

  void makeInactive(grid, Point p) {
    grid.remove(p.toString());
  }

  bool isActive(Point p) => _grid.containsKey(p.toString());

  void updateState(int cycle) {
    var xRange = [xMinMax[0] - cycle - 1, xMinMax[1] + cycle + 1];
    var yRange = [yMinMax[0] - cycle - 1, yMinMax[1] + cycle + 1];
    var zRange = [zMinMax[0] - cycle - 1, zMinMax[1] + cycle + 1];

    // print('update state --------------');
    // print(xRange);
    // print(yRange);
    // print(zRange);

    var newGrid = <String, String>{};

    for (var x = xRange[0]; x <= xRange[1]; x++) {
      for (var y = yRange[0]; y <= yRange[1]; y++) {
        for (var z = zRange[0]; z <= zRange[1]; z++) {
          var updatePoint = Point(x, y, z);
          var activeCount = activeNeighbours(updatePoint);
          if (isActive(updatePoint)) {
            if (activeCount.isBetweenI(2, 3)) {
              makeActive(newGrid, updatePoint);
            }
          } else {
            if (activeCount == 3) makeActive(newGrid, updatePoint);
          }
        }
      }
    }
    // print('$newGrid\n${newGrid.length}');
    _grid = newGrid;
  }

  int run(int cycles) {
    for (var cycleCount = 0; cycleCount < cycles; cycleCount++) {
      updateState(cycleCount);
    }
    return activeCubes();
  }
}

void runPart1(String name, List input) {
  printHeader(name);
  var pd = PocketDimension(input);
  print(pd.run(6));
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day17-test.txt');
  MAIN_INPUT = fileAsString('../data/day17.txt');

  //Answer: 112
  runPart1('17 test part 1', TEST_INPUT);
  //Answer: 848
  runPart2('17 test part 2', TEST_INPUT);

  //Answer: 284
  runPart1('17 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('17 part 2', MAIN_INPUT);
}
