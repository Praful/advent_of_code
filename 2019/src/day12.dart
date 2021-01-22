import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';

/// Puzzle description: https://adventofcode.com/2019/day/12

const bool DEBUG = false;

class Moon {
  List<int> velocity = [0, 0, 0];
  List<int> position;
  List<int> originalPosition;
  List<int> originalVelocity;
  Moon(this.position) {
    originalPosition = List.from(position);
    originalVelocity = List.from(velocity);
  }

  void updatePosition([index]) {
    void update(index) => position[index] += velocity[index];

    if (index != null) {
      update(index);
    } else {
      range(0, position.length).forEach((i) => update(i));
    }
  }

  int get pot => position.map((i) => i.abs()).sum;
  int get kin => velocity.map((i) => i.abs()).sum;
  int get totalEnergy => pot * kin;

  @override
  String toString() => 'pos=$position, vel=$velocity';
}

class Space {
  final _input;
  List<Moon> moons;
  Space(this._input) {
    moons = parse(_input);
  }

  @override
  String toString() => moons.join('\n');

  // <x=3, y=5, z=-1>
  List<Moon> parse(input) {
    var regex = RegExp(r'x\=(?<x>-?\d*), y\=(?<y>-?\d*), z=(?<z>-?\d*)\>');
    var result = <Moon>[];
    regex.allMatches(input).forEach((m) => result.add(Moon([
          m.namedGroup('x').toInt(),
          m.namedGroup('y').toInt(),
          m.namedGroup('z').toInt()
        ])));
    return result;
  }

  void updateVelocities(moon1, moon2, index) {
    if (moon1.position[index] > moon2.position[index]) {
      moon1.velocity[index]--;
      moon2.velocity[index]++;
    } else if (moon1.position[index] < moon2.position[index]) {
      moon1.velocity[index]++;
      moon2.velocity[index]--;
    }
  }

  void updatePositions([index]) =>
      moons.forEach((moon) => moon.updatePosition(index));

  int totalEnergy() => moons.map((m) => m.totalEnergy).sum;

  //Part 1
  int simulateMotion(timeSteps) {
    range(0, timeSteps).forEach((_) {
      Combinations(2, moons)().forEach((pair) {
        range(0, pair[0].position.length)
            .forEach((i) => updateVelocities(pair[0], pair[1], i));
      });
      updatePositions();
    });

    return totalEnergy();
  }

  bool matchesInitialState(index) =>
      moons.length ==
      moons
          .takeWhile((m) => (m.position[index] == m.originalPosition[index] &&
              m.velocity[index] == m.originalVelocity[index]))
          .length;

  int simulateXYorZ(index) {
    var timeStep = 1;
    while (true) {
      Combinations(2, moons)().forEach((pair) {
        updateVelocities(pair[0], pair[1], index);
      });
      updatePositions(index);

      if (matchesInitialState(index)) return timeStep;
      timeStep++;
    }
  }

  //Part 2
  int simulateUntilRepetition() {
    var timeStepX = simulateXYorZ(0);
    var timeStepY = simulateXYorZ(1);
    var timeStepZ = simulateXYorZ(2);

    return NumUtils.lcm(timeStepX, NumUtils.lcm(timeStepY, timeStepZ));
  }
}

void printAndAssert(actual, [expected]) {
  if (expected != null) {
    assertEqual(actual, expected);
  } else {
    print(actual);
  }
}

Object part1(String header, String input, int timeSteps) {
  printHeader(header);
  return Space(input).simulateMotion(timeSteps);
}

Object part2(String header, String input) {
  printHeader(header);
  return Space(input).simulateUntilRepetition();
}

void main(List<String> arguments) {
  var testInput = FileUtils.asString('../data/day12-test.txt');
  var testInputB = FileUtils.asString('../data/day12b-test.txt');
  var mainInput = FileUtils.asString('../data/day12.txt');

  assertEqual(part1('12 test part 1', testInput, 10), 179);
  assertEqual(part1('12 test part 1b', testInputB, 100), 1940);

  assertEqual(part2('12 test part 2', testInput), 2772);
  assertEqual(part2('12 test part 2b', testInputB), 4686774924);

  printAndAssert(part1('12 part 1', mainInput, 1000), 7202);
  printAndAssert(part2('12 part 2', mainInput), 537881600740876);
}
