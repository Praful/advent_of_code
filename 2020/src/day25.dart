import './utils.dart';

const bool DEBUG = false;

List TEST_INPUT;
List TEST_INPUT2;
List MAIN_INPUT;

const int DIVIDER = 20201227;

int findLoopSize(int publicKey, int subjectNumber) {
  print('key: $publicKey, subject: $subjectNumber');
  var generated = 1;
  var loopSize = 0;
  while (generated != publicKey) {
    loopSize++;
    generated = (generated * subjectNumber) % DIVIDER;
  }
  // print('generated: $generated');
  return loopSize;
}

int encryptonKey(int subjectNumber, int loopSize) {
  var result = 1;
  for (var i = 0; i < loopSize; i++) {
    result = (result * subjectNumber) % DIVIDER;
  }
  return result;
}

void runPart1(String name, List<String> input) {
  printHeader(name);
  var keys = input.map(int.parse).toList();
  var loopSize = keys.map((n) => findLoopSize(n, 7)).toList();
  print(loopSize);
  print(encryptonKey(keys[0], loopSize[1]));
  print(encryptonKey(keys[1], loopSize[0]));
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  TEST_INPUT = fileAsString('../data/day25-test.txt');
  MAIN_INPUT = fileAsString('../data/day25.txt');

  //Answer: 8, 11, 14897079
  runPart1('25 test part 1', TEST_INPUT);
  //Answer:
  // runPart2('25 test part 2', TEST_INPUT);

  //Answer: 9177528
  runPart1('25 part 1', MAIN_INPUT);
  //Answer:
  // runPart2('25 part 2', MAIN_INPUT);
}
