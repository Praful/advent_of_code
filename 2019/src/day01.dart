import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

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

int runPart1(String name, List<int> input) {
  printHeader(name);
  // return input.fold(0, (a, b) => a + fuelRequired(b));
  // return input.map((f) => fuelRequired(f)).sum; //alternative to above
  return input.fold2(fuelRequired); //another alt
}

int runPart2(String name, List<int> input) {
  printHeader(name);

  return input.fold2(recursiveFuelRequired); //another alt
  // return input.fold(0, (a, b) => a + recursiveFuelRequired(b));
  // return input.fold(0, (a, b) => a + loopFuelRequired(b));
}

void main(List<String> arguments) {
  TEST_INPUT = FileUtils.asInt('../data/day01-test.txt');
  MAIN_INPUT = FileUtils.asInt('../data/day01.txt');

  //Answer:34241
  print(runPart1('01 test part 1', TEST_INPUT));
  //Answer:51316
  print(runPart2('01 test part 2', TEST_INPUT));

  //Answer:3246455
  print(runPart1('01 part 1', MAIN_INPUT));
  //Answer:4866824
  print(runPart2('01 part 2', MAIN_INPUT));
}
