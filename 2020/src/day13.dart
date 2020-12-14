import './utils.dart';

const bool DEBUG = false;

String TEST_INPUT;
String MAIN_INPUT;

String OUT_OF_SERVICE = 'x';

//Example input file:
// 939
// 7,13,x,x,59,x,31,19
List parseInput1(input) {
  var raw = fileAsString(input);
  var departTime = int.parse(raw[0]);
  var busIds = raw[1]
      .split(',')
      .where((l) => l != OUT_OF_SERVICE)
      .map((id) => int.parse(id))
      .toList();
  return [departTime, busIds];
}

List parseInput2(input) {
  var raw = fileAsString(input);
  var busIds = raw[1]
      .split(',')
      .map((l) => l != OUT_OF_SERVICE ? int.parse(l) : l)
      .toList();
  return busIds;
}

void runPart1(String name, List input) {
  printHeader(name);
  var targetTime = input[0];
  List<int> buses = input[1];
  var nearestTimes =
      buses.map((id) => ((targetTime ~/ id) * id + id)).toList().cast<int>();
  var min = nearestTimes.min;
  print(buses[nearestTimes.indexOf(min)] * (min - targetTime));
}

void runPart2(String name, List input) {
  printHeader(name);

  // Remove x's. Create List of key/value pairs, where key is the bus's offset
  // and value is the bus ID.
  var buses =
      input.asMap().entries.where((e) => e.value != OUT_OF_SERVICE).toList();
  print(buses);

  bool busScheduled(bus, timestamp) => (timestamp + bus.key) % bus.value == 0;

  var timestamp = 0;
  var inc = 1;

  buses.forEach((bus) {
    while (!busScheduled(bus, timestamp)) {
      timestamp += inc;
    }
    inc *= bus.value;
  });

  print(timestamp);
}

void main(List<String> arguments) {
  TEST_INPUT = '../data/day13-test.txt';
  MAIN_INPUT = '../data/day13.txt';

  //Answer:295
  runPart1('13 test part 1', parseInput1(TEST_INPUT));

  runPart2('13 test part 2', parseInput2(TEST_INPUT)); //1068781
  runPart2('13 test part 2', [17, 'x', 13, 19]); //3417
  runPart2('13 test part 2', [67, 7, 59, 61]); //754018
  runPart2('13 test part 2', [67, 'x', 7, 59, 61]); //779210
  runPart2('13 test part 2', [67, 7, 'x', 59, 61]); //1261476
  runPart2('13 test part 2', [1789, 37, 47, 1889]); //1202161486

  //Answer:3464
  runPart1('13 part 1', parseInput1(MAIN_INPUT));
  //Answer: 760171380521445
  runPart2('13 part 2', parseInput2(MAIN_INPUT));
}
