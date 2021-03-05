import '../../shared/dart/src/utils.dart';
import './intcode_computer.dart';
import '../../shared/dart/src/grid.dart';

/// Puzzle description: https://adventofcode.com/2019/day/19

const bool DEBUG = false;

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

const BEAM_WIDTH = 50;
const BEAM_HEIGHT = BEAM_WIDTH;

int pointsInTractorBeam(program) {
  var coords = <int>[];
  for (var y in range(0, BEAM_HEIGHT)) {
    for (var x in range(0, BEAM_WIDTH)) {
      coords.add(x);
      coords.add(y);
    }
  }
  var result = 0;
  var drone = Computer(program, () => coords.removeAt(0));
  var originalState = drone.state;
  var beam = StringBuffer();
  var line = 0;
  var sentY = false;
  while (coords.isNotEmpty) {
    drone.run([], true);
    var output = drone.output(true);
    if (output.isNotEmpty) {
      if (output.first == 1) result++;
      if (beam.length == BEAM_WIDTH ) {
        print('${line.toString().padLeft(2, '0')} $beam');
        beam.clear();
        line++;
      }
      beam.write(output.first == 1 ? '#' : '.');
    }
    sentY = !sentY;
    drone.state = originalState; //reset program
  }
  return result;
}

Object part1(String header, List input) {
  printHeader(header);

  return pointsInTractorBeam(input);
}

Object part2(String header, List input) {
  printHeader(header);

  //TODO return something
  return null;
}

void main(List<String> arguments) {
  // List testInput = FileUtils.asLines('../data/day19-test.txt');
  List mainInput = FileUtils.asInt('../data/day19.txt', ',');

  // assertEqual(part1('19 test part 1', testInput), 1);
  // assertEqual(part2('19 test part 2', testInput), 1);

  printAndAssert(part1('19 part 1', mainInput));
  // printAndAssert(part2('19 part 2', mainInput));
}
