import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

class Point {
  final int x;
  final int y;
  final int z;
  final int w;
  Point(this.x, this.y, this.z, this.w);

  @override
  String toString() => '$x,$y,$z,$w';
  static Point toPoint(String s) {
    var coord = s.split(',').map((c) => int.parse(c)).toList();
    return Point(coord[0], coord[1], coord[2], coord[3]);
  }

  @override
  bool operator ==(covariant Point other) =>
      x == other.x && y == other.y && z == other.z && w == other.w;
}

class PocketDimension {
  List input;
  Map<String, String> _grid = {};
  static const String ACTIVE = '#';
  static const String INACTIVE = '.';

  var xMinMax;
  var yMinMax;
  var zMinMax;
  var wMinMax;

  PocketDimension(this.input) {
    toGrid();
  }

  String toKey(x, y, z, w) => Point(x, y, z, w).toString();

  void toGrid() {
    var x = 0, y = 0, z = 0, w = 0;

    input.forEach((row) {
      row.split('').forEach((c) {
        if (c == ACTIVE) makeActive(_grid, Point(x, y, z, w));
        x += 1;
      });
      x = 0;
      y += 1;
    });
    xMinMax = [0, input[0].length - 1];
    yMinMax = [0, input.length - 1];
    zMinMax = [0, 0];
    wMinMax = [0, 0];
  }

  @override
  String toString() => '$_grid';

  int activeCubes() => _grid.keys.length;

  int activeNeighbours(Point target) {
    var activeCount = 0;
    for (var x = target.x - 1; x < target.x + 2; x++) {
      for (var y = target.y - 1; y < target.y + 2; y++) {
        for (var z = target.z - 1; z < target.z + 2; z++) {
          for (var w = target.w - 1; w < target.w + 2; w++) {
            var neighbour = Point(x, y, z, w);
            if (target == neighbour) continue;
            if (isActive(neighbour)) activeCount++;
          }
        }
      }
    }
    return activeCount;
  }

  void makeActive(grid, Point p) => grid[p.toString()] = ACTIVE;

  bool isActive(Point p) => _grid.containsKey(p.toString());

  void updateState(int cycle) {
    //For each update, we look further out to either side of all axes.
    var xRange = [xMinMax[0] - cycle - 1, xMinMax[1] + cycle + 1];
    var yRange = [yMinMax[0] - cycle - 1, yMinMax[1] + cycle + 1];
    var zRange = [zMinMax[0] - cycle - 1, zMinMax[1] + cycle + 1];
    var wRange = [wMinMax[0] - cycle - 1, wMinMax[1] + cycle + 1];

    var newGrid = <String, String>{};

    for (var x = xRange[0]; x <= xRange[1]; x++) {
      for (var y = yRange[0]; y <= yRange[1]; y++) {
        for (var z = zRange[0]; z <= zRange[1]; z++) {
          for (var w = wRange[0]; w <= wRange[1]; w++) {
            var updatePoint = Point(x, y, z, w);
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
    }
    _grid = newGrid;
  }

  int run(int cycles) {
    for (var cycleCount = 0; cycleCount < cycles; cycleCount++) {
      updateState(cycleCount);
    }
    return activeCubes();
  }
}

void runPart2(String name, List input) {
  printHeader(name);
  var pd = PocketDimension(input);
  print(pd.run(6));
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day17-test.txt');
  MAIN_INPUT = fileAsString('../data/day17.txt');

  //Answer: 848
  runPart2('17 test part 2', TEST_INPUT);

  //Answer: 2240
  runPart2('17 part 2', MAIN_INPUT);
}
