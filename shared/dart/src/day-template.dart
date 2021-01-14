import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

Object runPart1(String name, List input) {
  printHeader(name);
}

Object runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsLines('../data/dayXX-test.txt');
  MAIN_INPUT = fileAsLines('../data/dayXX.txt');

  //Answer:
  print(runPart1('XX test part 1', TEST_INPUT));
  //Answer:
  // print(runPart2('XX test part 2', TEST_INPUT));

  //Answer:
  // print(runPart1('XX part 1', MAIN_INPUT));
  //Answer:
  // print(runPart2('XX part 2', MAIN_INPUT));
}
