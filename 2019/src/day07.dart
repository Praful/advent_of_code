import '../../shared/dart/src/utils.dart';
import 'package:trotter/trotter.dart';
import './intcode_computer.dart';

/// Puzzle description: https://adventofcode.com/2019/day/7

const bool DEBUG = false;

List run(program, input) {
  return Computer(program).run(0, input);
}

Object part1(String header, List input) {
  printHeader(header);
  // print(input);
  var perms = Permutations(5, range(0, 5).toList());
  return perms().map((phase) {
    var signal = 0;
    for (var i in range(0, 5)) {
      signal = run(input, [phase[i], signal]).first;
    }
    return signal;
  }).max;
}

Object part2(String header, List input) {
  printHeader(header);
}

void main(List<String> arguments) {
  List testInput = FileUtils.asInt('../data/day07-test.txt', ',');
  List testInputb = FileUtils.asInt('../data/day07b-test.txt', ',');
  List testInputc = FileUtils.asInt('../data/day07c-test.txt', ',');
  List mainInput = FileUtils.asInt('../data/day07.txt', ',');

  assertEqual(part1('07 test part 1', testInput), 43210);
  assertEqual(part1('07 test part 1b', testInputb), 54321);
  assertEqual(part1('07 test part 1c', testInputc), 65210);

  // assertEqual(part2('07 test part 2', testInput), 1);

  //Answer: 13848
  print(part1('07 part 1', mainInput));
  //Answer:
  // print(part2('07 part 2', mainInput));
}
