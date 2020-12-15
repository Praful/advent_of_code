import './utils.dart';

const bool DEBUG = false;
const int TURN_COUNT = 2020;
// const int TURN_COUNT = 30000000;
// const int TURN_COUNT = 11;

void runPart1(String name, List<int> input) {
  printHeader(name);

  var history = <int, List<int>>{};
  for (var i = 0; i < input.length - 1; i++) history[input[i]] = [i + 1];

  var lastNumberSpoken = input.last;
  for (var turn = input.length + 1; turn <= TURN_COUNT; turn++) {
    if (DEBUG) print('$turn: last number is $lastNumberSpoken');

    var occurrences = history[lastNumberSpoken] ?? [];

    if (occurrences.isEmpty) {
      occurrences.add(turn - 1);
      history[lastNumberSpoken] = occurrences;
      lastNumberSpoken = 0;
    } else {
      lastNumberSpoken = (turn - 1) - occurrences.max;
      occurrences.add(turn - 1);
    }
    if (DEBUG) print('--- speak $lastNumberSpoken');
  }
  if (DEBUG) print(history);
  print(lastNumberSpoken);
}

void runPart2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  //Answer: 436
  runPart1('15 test part 1', [0, 3, 6]);

  runPart1('15 test part 1a', [1, 3, 2]); // 2020th number spoken is 1.
  runPart1('15 test part 1b', [2, 1, 3]); // 2020th number spoken is 10.
  runPart1('15 test part 1c', [1, 2, 3]); // 2020th number spoken is 27.
  runPart1('15 test part 1d', [2, 3, 1]); // 2020th number spoken is 78.
  runPart1('15 test part 1e', [3, 2, 1]); // 2020th number spoken is 438.
  runPart1('15 test part 1f', [3, 1, 2]); // 2020th number spoken is 1836.

  //Answer:
  // runPart2('15 test part 2', TEST_INPUT);

  //Answer: 1696
  runPart1('15 part 1', [12, 1, 16, 3, 11, 0]);
  //Answer:
  // runPart2('15 part 2', MAIN_INPUT);
}
