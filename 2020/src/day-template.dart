import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

void runPart1(String name, List input) {
  printHeader(name);
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day12-test.txt');
  MAIN_INPUT = fileAsString('../data/day12.txt');

  //Answer:
  runPart1('12 test part 1', TEST_INPUT);
  //Answer:
  runPart2('12 test part 2', TEST_INPUT);

  //Answer:
  runPart1('12 part 1', MAIN_INPUT);
  //Answer:
  runPart2('12 part 2', MAIN_INPUT);
}
