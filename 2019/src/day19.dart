import '../../shared/dart/src/utils.dart';
import 'dart:math';
import './intcode_computer.dart';
// import '../../shared/dart/src/grid.dart';

/// Puzzle description: https://adventofcode.com/2019/day/19

const bool DEBUG = false;

int part2Value(x, y) => (x * 10000) + y;

String pad(nStr, width) => nStr.toString().padLeft(width, '0');

int beamWidth(StringBuffer beam) =>
    beam.toString().lastIndexOf('#') - beam.toString().indexOf('#') + 1;

List<int> beamStartEnd(StringBuffer beam) =>
    [beam.toString().indexOf('#'), beam.toString().lastIndexOf('#')];

List<int> pointToList(Point p) => [p.x.toInt(), p.y.toInt()];
Point listToPoint(List<int> l) => Point(l[0], l[1]);

//return vertices where p is the top left of a square of size n
List<Point> generateSquare(Point p, int n) {
  var width = n - 1;
  return [
    p,
    Point(p.x + width, p.y),
    Point(p.x, p.y + width),
    Point(p.x + width, p.y + width)
  ];
}

var beamMemo = <Point, bool>{};
bool inTractorBeam(Point p, program) {
  var result = beamMemo[p];
  if (result == null) {
    var coords = pointToList(p);
    var drone = Computer(program, () => coords.removeAt(0));
    drone.run([], true);

    result = drone.output(true).first == 1;
    beamMemo[p] = result;
  }
  // print('$p, $result');
  return result;
}

int pointsInTractorBeam(List<int> coords, program, int width) {
  var result = 0;
  var beam = StringBuffer();
  while (coords.isNotEmpty) {
    var x = coords[0];
    var y = coords[1];
    var drone = Computer(program, () => coords.removeAt(0));
    drone.run([], true);
    var output = drone.output(true);
    if (output.first == 1) result++;
    beam.write(output.first == 1 ? '#' : '.');
    if (beam.length == width) {
      // print( '${pad(x, 3)} ${pad(coords.length, 5)} ${pad(beamWidth(beam), 3)} $beam');
      // print( '${pad(x, 4)} ${beamStartEnd(beam)} ${pad(beamWidth(beam), 3)} $beam');
      print('${pad(x, 4)} $beam');
      beam.clear();
    }
  }
  return result;
}

int part1(String header, List input) {
  printHeader(header);

  const BEAM_WIDTH = 50;
  const BEAM_HEIGHT = BEAM_WIDTH;

  var coords = <int>[];
  for (var x in range(0, BEAM_WIDTH)) {
    for (var y in range(0, BEAM_HEIGHT)) {
      coords.add(x);
      coords.add(y);
    }
  }
  return pointsInTractorBeam(coords, input, BEAM_WIDTH);
}

int part2(String header, List input) {
  printHeader(header);
  //Determined empirically; probably should use something like binary search
  //to make it quicker. Currently takes about 3 minutes.
  var xRange = [700, 1100];
  var yRange = [700, 1100];
  var width = 100;

  var count = 0;
  for (var x in range(xRange[0], xRange[1])) {
    for (var y in range(yRange[0], yRange[1])) {
      var square = generateSquare(Point(x, y), width);
      if (square.every((vertex) => inTractorBeam(vertex, input))) {
        print(square);
        return part2Value(x, y);
      }
      if (count++ % 5000 == 0) print('$x, $y');
    }
  }
  throw 'Part 2 value not found';
}

//used to narrow down where to start looking for square
// int part2a(String header, List input) {
//   printHeader(header);

//   var xRange = [900, 1300];
//   var yRange = [700, 900];

//   var coords = <int>[];
//   for (var x in range(xRange[0], xRange[1])) {
//     for (var y in range(yRange[0], yRange[1])) {
//       coords.add(x);
//       coords.add(y);
//     }
//   }

// return pointsInTractorBeam(coords, input, yRange[1] - yRange[0]);
// }

void main(List<String> arguments) {
  var mainInput = FileUtils.asInt('../data/day19.txt', ',');

  printAndAssert(part1('19 part 1', mainInput), 231);
  printAndAssert(part2('19 part 2', mainInput), 9210745);
}
