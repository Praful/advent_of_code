import '../../shared/dart/src/utils.dart';

/// Puzzle description: https://adventofcode.com/2019/day/6

const bool DEBUG = false;

//Return number of objects orbited by object
int orbitCount(Map orbits, object) {
  var total = 0;
  var orbitedObject = orbits[object];
  if (orbitedObject != null) total = orbitCount(orbits, orbitedObject) + 1;
  return total;
}

//Return list of objects orbited by object.
List orbitedObjects(Map orbits, object) {
  var total = [];
  var orbitedObject = orbits[object];
  if (orbitedObject != null) {
    total
      ..add(orbitedObject)
      ..addAll(orbitedObjects(orbits, orbitedObject));
  }
  return total;
}

//key = orbiting object, value = orbited object
Map orbitMap(input) => {for (var o in input) o.split(')')[1]: o.split(')')[0]};
//part 1 alternative that uses the method for part 2
int part1Alternative(String header, List input) {
  printHeader(header);
  var orbits = orbitMap(input);
  return orbits.keys
      .fold(0, (sum, o) => sum + orbitedObjects(orbits, o).length);
}

int part1(String header, List input) {
  printHeader(header);
  var orbits = orbitMap(input);
  return orbits.keys.fold(0, (sum, o) => sum + orbitCount(orbits, o));
  // return part1Alternative(header, input);
}

int part2(String header, List input) {
  printHeader(header);
  var orbits = orbitMap(input);
  var youOrbits = orbitedObjects(orbits, 'YOU');
  var sanOrbits = orbitedObjects(orbits, 'SAN');
  var bothOrbit = youOrbits.toSet().intersection(sanOrbits.toSet());
  return (youOrbits.indexOf(bothOrbit.first)) +
      (sanOrbits.indexOf(bothOrbit.first));
}

void main(List<String> arguments) {
  List testInput = FileUtils.asLines('../data/day06-test.txt');
  List testInputb = FileUtils.asLines('../data/day06b-test.txt');
  List mainInput = FileUtils.asLines('../data/day06.txt');

  //Answer:
  assertEqual(part1('06 test part 1', testInput), 42);
  //Answer:
  assertEqual(part2('06 test part 2', testInputb), 4);

  //Answer:171213
  print(part1('06 part 1', mainInput));
  //Answer: 292
  print(part2('06 part 2', mainInput));
}
