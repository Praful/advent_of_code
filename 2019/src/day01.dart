import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/1

const bool DEBUG = false;

int recursiveFuelRequired(int mass) {
  var fuel = fuelRequired(mass);
  return (fuel <= 0) ? 0 : fuel + recursiveFuelRequired(fuel);
}

//alternative to above using a while loop
int loopFuelRequired(int mass) {
  var result = 0;
  var calcMass = mass;

  while (true) {
    var fuel = fuelRequired(calcMass);
    if (fuel <= 0) break;
    result += fuel;
    calcMass = fuel;
  }

  if (DEBUG) print('Total for $mass: $result');
  return result;
}

int fuelRequired(int mass) {
  var result = (mass / 3).floor() - 2;
  if (DEBUG) print('$mass: $result');
  return result;
}

int part1(String header, List<int> input) {
  printHeader(header);
  // return input.fold(0, (a, b) => a + fuelRequired(b));
  // return input.map((f) => fuelRequired(f)).sum; //alternative to above
  return input.fold2(fuelRequired) as int; //another alt
}

int part2(String header, List<int> input) {
  printHeader(header);

  return input.fold2(recursiveFuelRequired) as int; //another alt
  // return input.fold(0, (a, b) => a + recursiveFuelRequired(b));
  // return input.fold(0, (a, b) => a + loopFuelRequired(b));
}

void main(List<String> arguments) {
  var testInput = FileUtils.asInt('../data/day01-test.txt');
  var mainInput = FileUtils.asInt('../data/day01.txt');

  assertEqual(part1('01 test part 1', testInput), 34241);
  assertEqual(part2('01 test part 2', testInput), 51316);

  //Answer:3246455
  printAndAssert(part1('01 part 1', mainInput),3246455);
  //Answer:4866824
  printAndAssert(part2('01 part 2', mainInput),4866824);
}
