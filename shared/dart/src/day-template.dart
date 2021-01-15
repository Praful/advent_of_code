import '../../shared/dart/src/utils.dart';

const bool DEBUG = false;

Object part1(String name, List input) {
  printHeader(name);
}

Object part2(String name, List input) {
  printHeader(name);
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/dayXX-test.txt');
  List mainInput = FileUtils.asLines('../data/dayXX.txt');

  //Answer:
  print(part1('XX test part 1', testInput));
  //Answer:
  // print(part2('XX test part 2', testInput));

  //Answer:
  // print(part1('XX part 1', mainInput));
  //Answer:
  // print(part2('XX part 2', mainInput));
}
